# skyporten_workload_identity


Denne mappen inneholder en Terraform-modul som har som mål å dele tilgang til gcp-bøtter ved autentisering igjennom skyporten.

Modulen setter opp workload identity federation for Oauth2/OIDC-integrasjon mot skyporten. Det lages en workload identity pool, og poolen settes til å stole på skyporten.
Les mer om skyporten her: https://docs.digdir.no/docs/Maskinporten/maskinporten_skyporten.html.


Modulen tar inn en liste med organisasjonsnummer, og for hvert nummer opprettes det en bøtte i gcp. Hvert organisasjonsnummer autentisert igjennom skyporten gis lesetilgang til sin dedikerte gcp-bøtte. Bøttene får tilfeldige navn som outputtes av modulen.

## Eksempelbruk av modulen

```hcl
module "skyporten_integration" {
  source = "git::https://github.com/kartverket/dask-modules//terraform/modules/skyporten_workload_identity?ref=<version_numer>"

  workload_pool_id                    = "skyporten-${var.environment}"
  provider_id                         = "skyporten-provider-${var.environment}"
  required_audience                   = "https://skyporten.kartverk.no"
  main_scope                          = "kartverk"
  sub_scope                           = "test.scope"
  consumer_org_numbers                = ["992219688", "943753709"]
  project_number                      = var.project_number
  region                              = var.bucket_location
  project_id                          = var.project_id
  workload_identity_pool_display_name = "${var.environment}_pool"
  skyporten_env                       = var.environment

  providers = {
    google = google
  }
```

Legg merke til følgende parameter: 

- `skyporten_env`: Kan være enten `test` eller `prod`. Dette bestemmer om integrasjonen opprettes mot skyportens test- eller prodmiljø. 
- `main/sub_scope`: må opprettes via digdir eller giennom skip. https://sjolvbetjening.test.samarbeid.digdir.no/login