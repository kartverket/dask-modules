# Module for creating a service account for running Databricks jobs.
# Add the service account as an "external user" in dask-infrastructure to get necessary Databricks access:
# https://github.com/kartverket/dask-infrastructure/blob/main/terraform/modules/product_teams/main.tf#L11

resource "google_service_account" "dbx_job_runner" {
  account_id   = "databricks-job-runner"
  display_name = "My Service Account"
}

# Service account GCP access for landing zone and catalog buckets
resource "google_storage_bucket_iam_member" "lz_legacy_bucket_reader" {
  bucket = "landing-zone-${var.project_id}"
  role   = "roles/storage.legacyBucketReader"
  member = "serviceAccount:${google_service_account.dbx_job_runner.email}"
}

resource "google_storage_bucket_iam_member" "lz_object_admin" {
  bucket = "landing-zone-${var.project_id}"
  member = "serviceAccount:${google_service_account.dbx_job_runner.email}"
  role   = "roles/storage.objectAdmin"
}

resource "google_storage_bucket_iam_member" "catalog_legacy_bucket_reader" {
  bucket = "catalog-${var.project_id}"
  role   = "roles/storage.legacyBucketReader"
  member = "serviceAccount:${google_service_account.dbx_job_runner.email}"
}

resource "google_storage_bucket_iam_member" "catalog_object_admin" {
  bucket = "catalog-${var.project_id}"
  member = "serviceAccount:${google_service_account.dbx_job_runner.email}"
  role   = "roles/storage.objectAdmin"
}

# Service account access to product team catalog
resource "databricks_grant" "catalog_grant" {
  provider   = databricks.workspace
  principal  = google_service_account.dbx_job_runner.email
  privileges = ["ALL_PRIVILEGES"]
  catalog    = var.catalog_name
}