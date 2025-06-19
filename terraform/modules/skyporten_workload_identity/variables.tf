variable "workload_pool_id" {
  description = "The ID of the workload pool to be used for the Skyporten integration"
  type        = string
}

variable "workload_identity_pool_display_name" {
  description = "The display name of the workload identity pool"
  type        = string
}

variable "provider_id" {
  description = "The provider ID for the OICD identity pool provider"
  type        = string
}

variable "required_audience" {
  description = "The required audience for the OICD identity pool provider. Docs: https://docs.digdir.no/docs/idporten/oidc/oidc_func_aud.html"
  type        = string

}

variable "consumer_org_numbers" {
  description = "The organization numbers that should be allowed to access the Skyporten integration"
  type        = set(string)
}

variable "region" {
  description = "The region to deploy the resources in"
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
  default     = "kartverk"
  type        = string
}

variable "sub_scope" {
  description = "The sub scope for the Maskinporten client."
  type        = string
}

variable "skyporten_env" {
  description = "The environment to deploy the Skyporten integration in"
  type        = string

  validation {
    condition     = contains(["test", "prod"], var.skyporten_env)
    error_message = "The skyporten_env variable must be either 'test' or 'prod'."
  }
}

variable "attribute_condition" {
  description = "The attribute condition for the OICD identity pool provider. If not set, no condition will be applied."
  type        = string
  default     = ""

}
