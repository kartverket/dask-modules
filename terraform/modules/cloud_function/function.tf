# Compress the function source code into a ZIP file
data "archive_file" "function_zip" {
  type        = "zip"
  output_path = "${path.module}/lambda-files.zip"
  source_dir  = var.function_folder_location
  excludes    = var.excludes
}

# Upload the ZIP file to a GCS bucket
resource "google_storage_bucket_object" "function_zip" {
  name   = "${var.name}-${data.archive_file.function_zip.output_sha}.zip"
  bucket = var.bucket_id
  source = data.archive_file.function_zip.output_path
}

# Define the Cloud Function resource
resource "google_cloudfunctions2_function" "cloud_function" {
  name        = var.name
  location    = var.location
  description = var.description
  project     = var.project
  labels      = var.labels

  build_config {
    runtime     = var.runtime
    entry_point = var.entry_point

    source {
      storage_source {
        bucket = var.bucket_id
        object = google_storage_bucket_object.function_zip.name
      }
    }
  }

  service_config {
    available_memory      = var.available_memory
    min_instance_count    = var.min_instance_count
    max_instance_count    = var.max_instance_count
    timeout_seconds       = var.timeout_seconds
    environment_variables = var.environment_variables
    ingress_settings      = var.ingress_settings
    service_account_email = var.service_account_email
  }
}

# Grant permissions for invoking the function
resource "google_cloudfunctions2_function_iam_member" "invoker" {
  project        = var.project
  location       = var.location
  cloud_function = google_cloudfunctions2_function.cloud_function.name
  role           = "roles/cloudfunctions.invoker"
  member         = "serviceAccount:${var.service_account_email}"
}

# Define the Cloud Scheduler job that triggers the Cloud Function
resource "google_cloud_scheduler_job" "cloud_scheduler_job" {
  for_each         = { for idx, val in var.schedule_params : idx => val }
  name             = "invoke-${var.name}${each.value.body != null ? each.value.body.job_postfix : ""}"
  description      = "Schedule the HTTPS trigger for cloud function"
  schedule         = each.value.schedule
  time_zone        = "Europe/Oslo"
  project          = google_cloudfunctions2_function.cloud_function.project
  region           = google_cloudfunctions2_function.cloud_function.location
  attempt_deadline = "${var.timeout_seconds}s"

  http_target {
    uri         = google_cloudfunctions2_function.cloud_function.service_config[0].uri
    http_method = "POST"
    body        = base64encode(jsonencode(each.value.body))
    headers = {
      "Content-Type" = "application/json"
    }

    oidc_token {
      service_account_email = var.service_account_email
    }
  }

  depends_on = [
    google_cloudfunctions2_function.cloud_function
  ]
}
