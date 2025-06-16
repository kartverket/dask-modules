variable "region" {
  description = "The region to deploy the resources in"
  type        = string
}

variable "workload_identity_pool_id" {
  description = "The ID of the workload pool to be used for the Skyporten integration"
  type        = string
}

variable "maskinporten_client_id" {
  description = "The Maskinporten client ID for the consumer"
  type        = string
}

variable "project_number" {
  description = "The project number of the project"
  type        = string
}

variable "project_id" {
  description = "The project ID of the project"
  type        = string
}

variable "main_scope" {
  description = "The main organisation scope for the Maskinporten client."
  type        = string
  default     = "kartverk"
}

variable "sub_scope" {
  description = "The sub scope for the Maskinporten client."
  type        = string
}
