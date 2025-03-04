output "delta_sharing_config_url" {
  value       = var.recipient != "" ? databricks_recipient.db2open.tokens[0].activation_url : null
  sensitive   = true
  description = "URL to download the Delta Sharing configuration for the recipient."
}

output "databricks_recipient_name" {
  value       = var.recipient != "" ? databricks_recipient.db2open.name : null
  description = "Name of the Databricks recipient."
}

# Sensitive output containing tokens and sharing codes
output "databricks_recipient_data" {
  value = var.recipient != "" ? {
    tokens         = databricks_recipient.db2open[0].tokens
    sharing_code   = databricks_recipient.db2open[0].sharing_code
    activation_url = try(databricks_recipient.db2open.tokens[0].activation_url, "No activation URL available")
  } : null
  sensitive   = true
  description = "Data for the Databricks recipient."
}

output "external_share_name" {
  value       = databricks_share.ext_table_share.name
  description = "The name of the external share."
}
