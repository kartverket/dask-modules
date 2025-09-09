########## Google Storage Bucket and bucket object for the Cloud Function source code
resource "google_storage_bucket" "source_bucket" {
  name                        = "gcf-${var.name}-${var.project_id}"
  location                    = var.region
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
}

resource "archive_file" "function_source_zip" {
  type        = "zip"
  source_dir  = var.source_dir
  output_path = "${path.module}/${var.name}.zip"
}

resource "google_storage_bucket_object" "function_source" {
  name   = "${var.name}-source#${archive_file.function_source_zip.output_md5}.zip"
  bucket = google_storage_bucket.source_bucket.name
  source = archive_file.function_source_zip.output_path
}

########## Cloud Function and necessary permissions
resource "google_cloudfunctions2_function" "function" {
  name     = "${var.name}-function"
  location = var.region
  build_config {
    entry_point = "main"
    runtime     = var.runtime
    source {
      storage_source {
        bucket = google_storage_bucket.source_bucket.name
        object = google_storage_bucket_object.function_source.name
      }
    }
    service_account = "projects/${var.project_id}/serviceAccounts/${var.service_account_email}"
  }
  service_config {
    environment_variables = var.environment_variables
    service_account_email = var.service_account_email
  }
}

resource "google_cloud_run_service_iam_member" "scheduler_invoker" {
  project  = var.project_id
  location = google_cloudfunctions2_function.function.location
  service  = google_cloudfunctions2_function.function.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${var.service_account_email}"
}

########## Cloud Scheduler Job
resource "google_cloud_scheduler_job" "job" {
  name        = "${var.name}-scheduler-job"
  schedule    = var.schedule
  time_zone   = "Europe/Oslo"
  description = "Scheduler for the ${var.name} Cloud Function"
  http_target {
    uri         = google_cloudfunctions2_function.function.service_config[0].uri
    http_method = "POST"
    oidc_token {
      service_account_email = var.service_account_email
    }
  }
}
