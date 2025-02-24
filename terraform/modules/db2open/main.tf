resource "random_password" "db2opensharecode" {
  count   = var.recipient != "" ? 1 : 0
  length  = 16
  special = true
}

resource "databricks_recipient" "db2open" {
  provider = databricks.workspace

  count               = var.recipient != "" ? 1 : 0
  name                = "recipient_${var.share_name}_${var.recipient}"
  comment             = "Recipient av db2open opprettet i Terraform for ${var.recipient}"
  authentication_type = "TOKEN"
  sharing_code        = random_password.db2opensharecode[0].result
}

resource "databricks_share" "ext_table_share" {
  provider = databricks.workspace
  name     = var.share_name

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

  count = var.recipient != "" ? 1 : 0

  grant {
    principal  = databricks_recipient.db2open[0].name
    privileges = ["SELECT"]
  }
}
