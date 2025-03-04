resource "random_password" "db2opensharecode" {
  length  = 16
  special = true
}

resource "databricks_recipient" "db2open" {
  name                = "recipient_${var.share_name}"
  comment             = "Recipient av db2open opprettet i Terraform for ${var.recipient}"
  authentication_type = "TOKEN"
  sharing_code        = random_password.db2opensharecode.result
}

resource "databricks_share" "ext_table_share" {
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
  share = databricks_share.ext_table_share.name

  grant {
    principal  = databricks_recipient.db2open.name
    privileges = ["SELECT"]
  }
}
