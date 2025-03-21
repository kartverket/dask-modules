variable "topic_name" {
  description = "The name of the topic that will be created"
  type = string
}

variable "publisher_service_account" {
  description = "The service account used for publishing messages to the topic"
  type = string
}

variable "project_id" {
  description = "The ID of the GCP project in which the resource belongs"
  type = string
}
