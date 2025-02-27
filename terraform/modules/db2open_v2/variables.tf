variable "recipient" {
  description = "List of valid recipient organization numbers."
}

variable "schema_name_ext" {
  type        = string
  description = "The schema name to share."
}

variable "tables_to_share" {
  type        = list(string)
  default     = []
  description = "List of tables to share"
}

variable "share_name" {
  description = "Name of share"
  type        = string
}

# Rotate.tf env vars

variable "google_cloud_project" {
  type = string
}
variable "region" {
  type    = string
  default = "europe-west1"
}

variable "databricks_host" {
  type = string
}

variable "bucket_name" {
  description = "Cloud Storage bucket name for storing the function source archive"
  type        = string
}

variable "token_file_name" {
  description = "Filename used by your Python script for writing tokens"
  type        = string
}

variable "scheduler_service_account_email" {
  description = "Service account that Cloud Scheduler will use to invoke the Cloud Function"
  type        = string
}

variable cron_schedule {
    description = "Cron schedule for the Cloud Scheduler job"
    type        = string
    default     = "29 13 * * *"
}