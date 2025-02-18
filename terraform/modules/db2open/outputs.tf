output "delta_sharing_config_urls" {
  value = {
    for key, recipient in databricks_recipient.db2open :
    key => recipient.tokens[0].activation_url
  }
  sensitive   = true
  description = "URLs to download the Delta Sharing configuration for each recipient."
}

output "databricks_recipient_names" {
  value = {
    for key, recipient in databricks_recipient.db2open :
    key => recipient.name
  }
  description = "Mapping of Databricks recipients."
}

# Sensitive output containing tokens and sharing codes
output "databricks_recipient_data" {
  value = {
    for key, recipient in databricks_recipient.db2open :
    key => {
      tokens         = recipient.tokens
      sharing_code   = recipient.sharing_code
      activation_url = try(recipient.tokens[0].activation_url, "No activation URL available")
    }
  }
  sensitive   = true
  description = "Data for each Databricks recipient."
}


output "external_share_name" {
  value       = databricks_share.ext_table_share
  description = "The name of the external share."
}
