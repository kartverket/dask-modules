# db2open_v2


Denne mappen inneholder en Terraform-modul som aktiverer Delta Sharing på et gitt sett med tabeller.


Modulen tar imot en liste av tabeller som skal deles, `tables_to_share`. Modulen aktiverer Delta Sharing på disse. Det genereres et token for tilgang til de Delta-sharet. Tokenet lagres i den spesifiserte bøtten. Det lages en Cloud Function som kjører med et regelmessig intervall gitt av input-feltet `cron_schedule`. Denne funksjonen roterer tokenet og lagrer det nye tokenet til den gitte bøtten. Det genererte tokenet er satt til en levetid på 1 døgn.

## Eksempelbruk av modulen

```hcl
module "delta_share" {
  source = "git::https://github.com/kartverket/dask-modules//terraform/modules/db2open_v2?ref=<version_number>"

  recipient                       = "georg"
  schema_name_ext                 = "plattform_dataprodukter_sandbox.test_schema"
  tables_to_share                 = ["test_table_1", "test_table_2", "test_table_3" ]
  share_name                      = "test_share"
  google_cloud_project            = var.project_id
  region                          = var.region
  databricks_host                 = var.databricks_workspace_url
  bucket_name                     = google_storage_bucket.static_bucket.name
  token_file_name                 = "token.json"
  scheduler_service_account_email = var.deploy_service_account
  cron_shedule                    = "* * * * *"

  providers = {
    databricks = databricks.workspace
  }
}
```

Legg merke til følgende parameter: 

- `tables_to_share`: Her spesifiseres navnene til alle tabeller som skal deles. [databricks_share](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/share) terraform-ressursen forventer en liste og legger til tabeller i en share basert på den leksikografiske sorteringen av listen. Dette resulterer i at nye tabeller alltid må legges nederst i `tables_to_share`-listen. Dette kan også resultere i en duplikatfeil hvis du fjerner og legger til tabeller i `tables_to_share`-listen
- `cron_schedule`: Bestemmer hvor ofte token for tilgang til delta-sharen skal roteres. Settes denne lavere enn 1 gang i døgnet resulterer dette i perioder uten gyldig token, siden tokenets levetid er satt fast til 1 døgn. 