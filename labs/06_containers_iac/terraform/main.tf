# Lab 06 — Terraform with local providers only (no cloud account needed).
#   terraform init
#   terraform plan -out plan.out && terraform show -json plan.out > plan.json   # review the plan, not just the code
#   terraform apply plan.out
# Try: terraform plan -var dscr_threshold=1.30 — changing a container's environment forces a replacement
#      (delete + create, i.e. a restart). Read the plan before applying, every time.
# The Docker provider finds Docker Desktop or the local engine automatically; set DOCKER_HOST if yours is elsewhere.

terraform {
  required_version = ">= 1.5"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

provider "docker" {}

variable "dscr_threshold" {
  type    = string
  default = "1.25"
}

resource "docker_image" "decision" {
  name         = "decision-service:1.0.1"
  keep_locally = true
}

resource "docker_container" "decision" {
  name  = "decision-service"
  image = docker_image.decision.image_id
  env   = ["DSCR_THRESHOLD=${var.dscr_threshold}"]
  ports {
    internal = 8080
    external = 8081
  }
  healthcheck {
    test     = ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2)"]
    interval = "30s"
  }
}

resource "local_file" "runbook" {
  filename             = "${path.module}/RUNBOOK.generated.md"
  file_permission      = "0644" # the default is 0777: least privilege applies to files too
  directory_permission = "0755"
  content              = "Decision service on port 8081, threshold ${var.dscr_threshold}. Roll back: terraform apply the previous plan."
}

output "url" {
  value = "http://localhost:8081/health"
}
