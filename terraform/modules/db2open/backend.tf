terraform {
  required_providers {
    databricks = {
      source                = "databricks/databricks"
    }
    google = {
      source  = "hashicorp/google"
    }
    archive = {
      source  = "hashicorp/archive"
    }
  }
}
