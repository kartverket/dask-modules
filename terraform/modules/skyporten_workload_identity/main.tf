# Set up the IAM workload identity pool and provider for Skyporten integration
resource "google_iam_workload_identity_pool" "maskinporten" {
  workload_identity_pool_id = var.workload_pool_id
  display_name              = var.workload_pool_id
}

resource "google_iam_workload_identity_pool_provider" "maskinporten" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.maskinporten.workload_identity_pool_id
  workload_identity_pool_provider_id = var.provider_id
  attribute_mapping = {
    "attribute.maskinportenscope" = "assertion.scope"
    "google.subject"              = "assertion.consumer.ID"
    "attribute.clientaccess"      = "\"client::\" + assertion.consumer.ID + \"::\" + assertion.scope"
  }
  display_name = var.workload_identity_pool_display_name
  description  = "OIDC identity pool provider for Maskinporten"
  oidc {
    allowed_audiences = [var.required_audience]
    issuer_uri        = var.issuer_uri
  }
}

# Define consumers and access levels
module "skyporten_consumer" {
  source   = "./skyporten_consumers"
  for_each = var.consumer_org_numbers

  # 0192 is the prefix for Norwegian organizations
  maskinporten_client_id    = "0192:${each.key}"
  main_scope                = var.main_scope
  sub_scope                 = var.sub_scope
  region                    = var.region
  org_number                = each.key
  consumer_name             = each.value
  project_number            = var.project_number
  workload_identity_pool_id = google_iam_workload_identity_pool.maskinporten.workload_identity_pool_id
  project_id                = var.project_id

  providers = {
    google = google
  }

  depends_on = [google_iam_workload_identity_pool.maskinporten, google_iam_workload_identity_pool_provider.maskinporten]
}
