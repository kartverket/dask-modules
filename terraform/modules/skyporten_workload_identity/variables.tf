variable "workload_pool_id" {
  description = "The ID of the workload pool to be used for the Skyporten integration"
}

variable "workload_identity_pool_display_name" {
  description = "The display name of the workload identity pool"
}

variable "provider_id" {
  description = "The provider ID for the OICD identity pool provider"
}

variable "required_audience" {
  description = "The required audience for the OICD identity pool provider. Docs: https://docs.digdir.no/docs/idporten/oidc/oidc_func_aud.html"
}

variable "consumer_org_numbers" {
  description = "The organization numbers that should be allowed to access the Skyporten integration"
}

variable "region" {
  description = "The region to deploy the resources in"
}

variable "project_number" {
  description = "The project number of the project"
}

variable "project_id" {
  description = "The project ID of the project"
}


variable "issuer_uri" {
  description = "The issuer URI for the OICD identity pool provider"
}

variable "main_scope" {
  description = "The main organisation scope for the Maskinporten client."
  default     = "kartverk"
}

variable "sub_scope" {
  description = "The sub scope for the Maskinporten client."
}
