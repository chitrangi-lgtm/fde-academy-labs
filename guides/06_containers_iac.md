# Lab 06: A reviewer-proof container, Kubernetes and a Terraform plan

**Time:** 90 minutes · **Level:** Advanced · **Builds on:** Professional Practice P1, FDE Module 17 (deployment and infrastructure), FDE Module 16 (security)

## The problem

CrestFin's security team reviews every container before it reaches production. Last quarter they rejected three
images: one ran as root, one had an API key baked into a layer, and one used the `latest` tag, so nobody could say what
was actually deployed. The platform team also wants every infrastructure change made through Terraform, with the plan
reviewed before it is applied.

In this lab you package a small decision service in a container a reviewer will accept, deploy it to a local Kubernetes
cluster with **kind**, and manage a local deployment with **Terraform**, reading the plan before every change. Nothing
needs a cloud account.

## What you'll learn

- The Dockerfile practices security reviewers check: a pinned base image, a non-root user, no secrets, a health check.
- Why a service must handle `SIGTERM` to stop cleanly during a rolling update.
- How a Kubernetes Deployment, Service and HorizontalPodAutoscaler fit together, with probes, resource limits and a
  locked-down security context.
- How to produce and read a Terraform plan, and why a changed environment variable replaces a container.

## Before you start

You need Docker, [kind](https://kind.sigs.k8s.io/), kubectl and [Terraform](https://developer.hashicorp.com/terraform)
1.5 or later on your machine (this lab runs on your host, not inside the labs container). Work in
`realtools/labs/06_containers_iac/`.

## Key ideas

**Pin what you run.** `FROM python:3.12.7-slim` names an exact version, so a rebuild next month uses the same base. The
image itself is tagged `1.0.1`, never `latest`, so every deployment can be traced to a build.

**Run as an ordinary user.** `useradd --uid 10001 app` and `USER app` mean a compromised process has no root rights in
the container. The Kubernetes manifest backs this up with `runAsNonRoot`, `allowPrivilegeEscalation: false`, a
read-only root filesystem and all Linux capabilities dropped.

**Health checks drive automation.** The Dockerfile's `HEALTHCHECK` and the Kubernetes readiness and liveness probes call
`/health`. Readiness decides whether a pod receives traffic; liveness restarts a stuck pod.

**Stop promptly on SIGTERM.** As process 1 in a container, Python ignores `SIGTERM` unless a handler is installed.
Kubernetes would then wait the full grace period (30 seconds) before killing the pod. `app.py` installs a handler that
exits at once, so rolling updates are quick.

**Plans before applies.** `terraform plan -out plan.out` records exactly what will change. Reviewing the plan, not just
the code, catches surprises such as a resource being destroyed and recreated.

## Steps

1. **Build and run the image.** `docker build -t decision-service:1.0.1 .` then
   `docker run --rm -p 8080:8080 decision-service:1.0.1`. In another terminal:
   `curl localhost:8080/health` returns `{"status": "ok"}`, and
   `curl -X POST localhost:8080/decide -d '{"ebitda": 1500000, "debt_service": 1100000}'` returns
   `{"dscr": 1.36, "decision": "APPROVE"}`.

2. **Check what a reviewer checks.** Run `docker run --rm decision-service:1.0.1 id` and confirm `uid=10001(app)`.
   Run `docker history decision-service:1.0.1` and confirm no layer contains a secret. Run `docker inspect` and find the
   health check.

3. **Deploy to kind.** `kind create cluster --name fde`, `kind load docker-image decision-service:1.0.1 --name fde`,
   `kubectl apply -f k8s/`, then `kubectl get pods -w` until both pods are `Running` and ready (`1/1`). Port-forward with
   `kubectl port-forward svc/decision-service 8080:80` and call `/decide` again.

4. **Roll out a change.** Change `DSCR_THRESHOLD` to `"1.40"` in `k8s/deployment.yaml` and apply. Watch the rolling update
   with `kubectl rollout status deployment/decision-service`: new pods start and become ready before old ones stop
   (`maxUnavailable: 0`). The same request now returns `REFER`, because 1.36 is below 1.40.

5. **See why SIGTERM matters.** Comment out `signal.signal(signal.SIGTERM, _stop)`, rebuild as `1.0.2`, load it, update
   the image tag and roll out. Time how long old pods take to disappear (about 30 seconds each instead of about 1). Restore
   the handler.

6. **Plan with Terraform.** In `terraform/`: `terraform init`, then `terraform plan -out plan.out`. Read the plan: a
   Docker image, a container on port 8081 and a runbook file. Apply it with `terraform apply plan.out` and check
   `curl localhost:8081/health`.

7. **Read a replacement.** Run `terraform plan -var dscr_threshold=1.30`. The plan shows the container `must be replaced`
   (`-/+`) because its environment changed. That means a restart. In a review, this line is the one to discuss.

8. **Clean up.** `terraform destroy`, `kind delete cluster --name fde`.

## Check yourself

<details><summary>Why does changing an environment variable replace the container?</summary>
A running container's environment can't be changed. Terraform's Docker provider has to delete the container and create
a new one with the new value, which means a brief outage unless something else is serving traffic.
</details>

<details><summary>What is the difference between the readiness and liveness probes?</summary>
Readiness says whether the pod should receive traffic now; failing it removes the pod from the Service without restarting
it. Liveness says whether the process is healthy; failing it makes Kubernetes restart the container.
</details>

<details><summary>Why does the HorizontalPodAutoscaler show unknown CPU in kind?</summary>
It reads CPU usage from metrics-server, which kind doesn't install. Install metrics-server and the target shows real
utilisation.
</details>

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `ErrImagePull` or `ImagePullBackOff` in kind | The image is only in your local Docker, not in the cluster | `kind load docker-image decision-service:1.0.1 --name fde` and keep `imagePullPolicy: IfNotPresent` |
| Pods crash with a read-only filesystem error | The app tries to write to its root filesystem | Write only to a mounted `emptyDir` volume, or keep the app stateless as here |
| `terraform plan` can't connect to Docker | The Docker provider can't find the engine | Start Docker Desktop, or set `DOCKER_HOST` |
| Rolling updates are slow | The app ignores SIGTERM | Install a SIGTERM handler that exits promptly |

## Take it further

- Scan the image with Trivy and fix anything it reports as high or critical.
- Add a `PodDisruptionBudget` so at least one pod always stays up during node maintenance.
- Store Terraform state in a remote backend with locking, as a real team would.

## In a real client project

- Use the client's approved base images and private registry, and sign images in the build pipeline.
- Keep secrets in the platform's secret store, mounted at runtime, never in the image or the manifest.
- Require a reviewed plan for every infrastructure change, attached to the change request.
