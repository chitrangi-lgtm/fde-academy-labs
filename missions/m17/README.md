# Review the deployment before the client's security team does

**From:** Elif Yilmaz, Platform Security Engineer, Gantry Freight

Your team's container goes to our Kubernetes cluster next week. Our security review rejects deployments for the same handful of reasons every time, so please build the pre-check we'll run in CI: read the Dockerfile and the deployment manifest and report the codes from our standard list. I've attached your current files and a fixed version so you can see both outcomes.

## Done when

- `review(dockerfile_text, manifest)` returns the sorted list of finding codes that apply:
- ROOT_USER: no USER line, or the last USER is root or 0; LATEST_TAG: a FROM image with no tag or :latest
- NO_PROBES: the container lacks a readinessProbe or a livenessProbe; NO_LIMITS: resources.limits lacks cpu or memory
- SECRET_IN_ENV: an env var whose name contains KEY, SECRET, PASSWORD or TOKEN has a literal value instead of valueFrom
- PRIVILEGED: securityContext.privileged is true; WRITABLE_ROOT_FS: securityContext.readOnlyRootFilesystem is not true

## Files

`Dockerfile`, `deployment.json`, `Dockerfile.fixed`, `deployment.fixed.json`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m17
```

There are no steps: how you build it is up to you. If you are stuck, `NUDGES.md` has two hints. The course site's version of this challenge (Module m17) records your score.
