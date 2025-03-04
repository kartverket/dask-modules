# I main-modul. pass på at relevante APIer er aktivert
# resource "google_project_service" "activate_services" {
#   for_each = toset(["cloudfunctions.googleapis.com", "run.googleapis.com", "cloudbuild.googleapis.com", "cloudscheduler.googleapis.com", "storage.googleapis.com"])
#   project  = var.google_cloud_project
#   service  = each.value
# }

module "rotate_function" {
  count                 = var.recipient != "" ? 1 : 0
  source                = "git::https://github.com/kartverket/dask-modules//terraform/modules/cloud_function_v2?ref=v2.6.1"
  name                  = "rotate-${var.share_name}"
  project_id            = var.google_cloud_project
  region                = var.region
  runtime               = "python312"
  source_dir            = "${path.module}/scripts"
  schedule              = var.cron_schedule
  service_account_email = var.scheduler_service_account_email

  environment_variables = {
    DATABRICKS_HOST                   = var.databricks_host
    DATABRICKS_GOOGLE_SERVICE_ACCOUNT = var.scheduler_service_account_email
    BUCKET_NAME                       = var.bucket_name
    TOKEN_FILE_NAME                   = var.token_file_name
    DELTA_SHARE_NAME                  = var.share_name                       # <-- Add this variable
    DELTA_RECIPIENT_NAME              = databricks_recipient.db2open[0].name # <-- Add this variable
  }
}
