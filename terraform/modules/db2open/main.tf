locals {
  valid_recipients = compact(var.recipients) # Removes empty strings
}

resource "random_password" "db2opensharecode" {
  for_each = toset(local.valid_recipients)

  length  = 16
  special = true
}

resource "databricks_recipient" "db2open" {
  provider = databricks.workspace

  for_each = toset(local.valid_recipients)

  name                = "recipient_${var.share_name}_${each.key}"
  comment             = "Recipient av db2open opprettet i Terraform for ${each.key}"
  authentication_type = "TOKEN"
  sharing_code        = random_password.db2opensharecode[each.key].result
}

resource "databricks_share" "ext_table_share" {
  provider = databricks.workspace

  name = var.share_name

  dynamic "object" {
    for_each = var.tables_to_share
    content {
      name                        = "${var.schema_name_ext}.${object.value}"
      data_object_type            = "TABLE"
      history_data_sharing_status = "ENABLED"
    }
  }
}

resource "databricks_grants" "share_grants" {
  provider = databricks.workspace
  share    = databricks_share.ext_table_share.name

  count = length(databricks_recipient.db2open) > 0 ? 1 : 0

  dynamic "grant" {
    for_each = databricks_recipient.db2open
    content {
      principal  = grant.value.name
      privileges = ["SELECT"]
    }
  }
}
