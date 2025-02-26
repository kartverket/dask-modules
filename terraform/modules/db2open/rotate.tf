# Turn on the required APIs for the project
resource "google_project_service" "activate_services" {
  for_each = toset(["cloudfunctions.googleapis.com", "run.googleapis.com"])
  project  = var.google_cloud_project
  service  = each.value
}

module "tilsyn_function" {
  source                = "git::https://github.com/kartverket/dask-modules//terraform/modules/cloud_function_v2?ref=v2.6.1"
  name                  = "tilsyn"
  project_id            = var.google_cloud_project
  region                = var.region
  runtime               = "python312"
  source_dir            = "${path.module}/scripts"
  schedule              = "29 13 * * *"
  service_account_email = var.scheduler_service_account_email

  environment_variables = {
    DATABRICKS_HOST                   = var.databricks_host
    DATABRICKS_GOOGLE_SERVICE_ACCOUNT = var.scheduler_service_account_email
    BUCKET_NAME                       = var.bucket_name
    TOKEN_FILE_NAME                   = var.token_file_name
    DELTA_SHARE_NAME                  = var.share_name                   # <-- Add this variable
    DELTA_RECIPIENT_NAME              = "dataplattform_deploy-recipient" # <-- Add this variable
  }
}
