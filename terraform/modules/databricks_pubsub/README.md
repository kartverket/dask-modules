# databricks_pubsub

Denne mappen inneholder en Terraform-modul som lager en PubSub topic og subscription som henter alle meldinger inn i en bronsetabell i Databricks.

NB! Kontoen din trenger `roles/iam.serviceAccountKeyAdmin` for å kunne opprette nøkkel i databricks for tilgang til kontoen som kjører modulen i PubSub.

## Eksempelbruk av modulen

```hcl
module "dbx_pubsub_poc" {
  source = "git::https://github.com/kartverket/dask-modules//terraform/modules/databricks_pubsub?ref=<version_number>"

  project_id                = var.project_id
  topic_name                = "dbx-pubsub-poc"
  publisher_service_account = var.deploy_service_account
  
  providers = {
    databricks = databricks.workspace
  }
}
```
