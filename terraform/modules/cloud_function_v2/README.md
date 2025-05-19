# cloud_function_v2

Denne mappen inneholder en Terraform-modul som lager en Cloud Function som kjører et script i henhold til en tidsplan.


Filer definert i `source_dir` lastes opp til en bøtte, og kjøres med entrypoint `main` i Cloud Functionen. Runtime brukt er definert i inputvariablen `runtime` og støtter følgende [verdier](https://cloud.google.com/run/docs/runtime-support#support_schedule). Det er ikke mulig å justere entrypoint, så alle script må ha en `main`-fil som kan brukes som entrypoint. 


## Eksempelbruk av modulen

Se [rotate.tf](../db2open_v2/rotate.tf). Generisk eksempel:

```hcl
module "example_function" {
  source                = "git::https://github.com/kartverket/dask-modules//terraform/modules/cloud_function_v2?ref=<version_number>"
  name                  = "example-function"
  project_id            = var.google_cloud_project
  region                = var.region
  runtime               = "python312"
  source_dir            = "${path.module}/example_function"
  schedule              = "* * * * *"
  service_account_email = var.scheduler_service_account_email

  environment_variables = {
    ENVIRONMENT_VARIABLES = "your script might need"
  }
}
```