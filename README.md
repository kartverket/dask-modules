# dask-modules
This repository contains Terraform modules maintained by DASK. The Terraform modules are used to provision infrastructure for teams being onboarded to the data platform.


### How to use the modules from other repos
Modules must be referenced in the source definition as follows:

````yaml
# Reference module defined in dbx_workspace_create
module "grant_access_to_table" {
  source   = "git::https://github.com/kartverket/dask-modules//terraform/modules/dbx_grant_table_access?ref=<hash/tag/branch>"
  # ...
}

````
Be aware of the double slash after `dask-modules`. This indicates to Terraform that the remaining path after `//` is a sub-directory within the package.
