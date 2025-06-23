locals {
  team_compute_sa = "databricks-compute@${var.project_id}.iam.gserviceaccount.com"
}

resource "google_pubsub_topic" "databricks_topic" {
  name = var.topic_name

  message_retention_duration = "2678400s"
}

resource "google_pubsub_subscription" "databricks_subscriptino" {
  name  = "${var.topic_name}-sub"
  topic = google_pubsub_topic.databricks_topic.name
}

resource "google_pubsub_topic_iam_member" "topic_member" {
  project = google_pubsub_topic.databricks_topic.project
  topic   = google_pubsub_topic.databricks_topic.name
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${var.publisher_service_account}"
}

resource "google_pubsub_subscription_iam_member" "sub_viewer" {
  project      = google_pubsub_topic.databricks_topic.project
  subscription = google_pubsub_subscription.databricks_subscriptino.name
  role         = "roles/pubsub.viewer"
  member       = "serviceAccount:${local.team_compute_sa}"
}

resource "google_pubsub_subscription_iam_member" "sub_consumer" {
  project      = google_pubsub_topic.databricks_topic.project
  subscription = google_pubsub_subscription.databricks_subscriptino.name
  role         = "roles/pubsub.subscriber"
  member       = "serviceAccount:${local.team_compute_sa}"
}

resource "google_service_account_key" "myki" {
  service_account_id = "databricks-compute"
}

resource "databricks_secret_scope" "pubsub_secret_scope" {
  name = "${google_pubsub_topic.databricks_topic.name}-scope"
}

resource "databricks_secret_acl" "pubsub_secret_acl" {
  principal  = local.team_compute_sa
  permission = "READ"
  scope      = databricks_secret_scope.pubsub_secret_scope.name
}

resource "databricks_secret" "pubsub_api" {
  key          = "pubsub-api"
  string_value = google_service_account_key.myki.private_key
  scope        = databricks_secret_scope.pubsub_secret_scope.name
}
