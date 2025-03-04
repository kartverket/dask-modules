locals {
  maskinporten_scope = "${var.main_scope}:${var.sub_scope}"
}

resource "random_string" "random" {
  length  = 4
  special = false
  upper   = false
}

resource "google_service_account" "skyporten_consumer" {
  account_id  = "sp-${var.org_number}-${random_string.random.result}"
  description = "Service account for the Skyporten consumer for organization ${var.org_number} with scope ${local.maskinporten_scope}"
}

data "google_iam_policy" "client_access" {
  binding {
    role = "roles/iam.workloadIdentityUser"

    members = [
      "principalSet://iam.googleapis.com/projects/${var.project_number}/locations/global/workloadIdentityPools/${var.workload_identity_pool_id}/attribute.clientaccess/client::${var.maskinporten_client_id}::${local.maskinporten_scope}",
    ]
  }
}

resource "google_service_account_iam_policy" "workload_identity_policy" {
  service_account_id = google_service_account.skyporten_consumer.name
  policy_data        = data.google_iam_policy.client_access.policy_data
}

resource "google_storage_bucket" "skyporten_bucket" {
  name                        = "sp-${var.project_id}-${random_string.random.result}"
  location                    = var.region
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_iam_member" "legacy_bucket_reader" {
  bucket = google_storage_bucket.skyporten_bucket.name
  role   = "roles/storage.legacyBucketReader"
  member = "serviceAccount:${google_service_account.skyporten_consumer.email}"
}

resource "google_storage_bucket_iam_member" "object_viewer" {
  bucket = google_storage_bucket.skyporten_bucket.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.skyporten_consumer.email}"
}

