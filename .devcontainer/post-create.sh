#!/usr/bin/env bash
# Runs once when the codespace (or dev container) is created. Everything here is free and open source.
set -euo pipefail

echo "== Python libraries for the labs, missions and Python labs"
pip install --user --no-cache-dir -r requirements.txt
pip install --user --no-cache-dir "moto[server]>=5,<6" boto3 pandas numpy scikit-learn pydantic duckdb networkx scipy \
  jsonschema matplotlib jupyterlab

echo "== kind (Kubernetes in Docker), pinned and checksum-verified"
KIND_VERSION=v0.33.0
mkdir -p "$HOME/.local/bin"
curl -fsSLo /tmp/kind "https://kind.sigs.k8s.io/dl/${KIND_VERSION}/kind-linux-amd64"
curl -fsSLo /tmp/kind.sha256 "https://github.com/kubernetes-sigs/kind/releases/download/${KIND_VERSION}/kind-linux-amd64.sha256sum"
(cd /tmp && echo "$(cut -d' ' -f1 kind.sha256)  kind" | sha256sum -c -)
install -m 0755 /tmp/kind "$HOME/.local/bin/kind"

cat <<'EOF'

FDE Academy labs are ready. Next:
  docker compose up -d --build                       # Qdrant, PostgreSQL + pgvector, OpenTelemetry, Jaeger
  docker compose exec labs python 02_vector_databases.py
  python tools/fde_check.py --list                   # challenge missions you can check here
Open START_HERE.md for the full guide, including the free cloud accounts you can connect.
EOF
