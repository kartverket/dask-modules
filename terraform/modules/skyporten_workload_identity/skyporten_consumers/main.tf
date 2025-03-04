locals {
  maskinporten_scope = "${var.main_scope}:${var.sub_scope}"
}

resource "random_string" "random" {
  length  = 4
  special = false
  upper   = false
}

resource "google_storage_bucket_iam_binding" "client_legacy_reader" {
  bucket = google_storage_bucket.skyporten_bucket.name
  role   = "roles/storage.legacyBucketReader"

  members = [
    "principalSet://iam.googleapis.com/projects/${var.project_number}/locations/global/workloadIdentityPools/${var.workload_identity_pool_id}/attribute.clientaccess/client::${var.maskinporten_client_id}::${local.maskinporten_scope}",
  ]
}

resource "google_storage_bucket_iam_binding" "client_object_viewer" {
  bucket = google_storage_bucket.skyporten_bucket.name
  role   = "roles/storage.objectViewer"

  members = [
    "principalSet://iam.googleapis.com/projects/${var.project_number}/locations/global/workloadIdentityPools/${var.workload_identity_pool_id}/attribute.clientaccess/client::${var.maskinporten_client_id}::${local.maskinporten_scope}",
  ]
}

resource "google_storage_bucket" "skyporten_bucket" {
  name                        = "sp-${var.project_id}-${random_string.random.result}"
  location                    = var.region
  uniform_bucket_level_access = true
}
