variable "use_emulator" {
  description = "true: point every AWS service at the local moto emulator (no account, no cost). false: a real AWS account."
  type        = bool
  default     = true
}

variable "emulator_url" {
  description = "Where moto_server is listening."
  type        = string
  default     = "http://localhost:5000"
}

variable "region" {
  description = "AWS region. eu-central-1 (Frankfurt) keeps EU customer data in the EU."
  type        = string
  default     = "eu-central-1"
}

variable "project" {
  description = "Short project name used in every resource name."
  type        = string
  default     = "crestfin-assist"
}

variable "environment" {
  description = "dev, test or prod."
  type        = string
  default     = "dev"
  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "environment must be dev, test or prod."
  }
}

variable "owner" {
  description = "The team accountable for these resources (appears in cost and access reviews)."
  type        = string
  default     = "fde-team"
}

variable "bucket_suffix" {
  description = "S3 bucket names are global; a suffix (your initials and a number) keeps yours unique."
  type        = string
  default     = "lab14"
}

variable "monthly_budget_usd" {
  description = "Real accounts only: alert when the month's forecast passes 80% of this."
  type        = string
  default     = "5"
}

variable "budget_email" {
  description = "Real accounts only: who receives the budget alert."
  type        = string
  default     = "you@example.com"
}
