variable "recipient" {
  description = "List of valid recipient organization numbers."
}

variable "schema_name_ext" {
  type        = string
  description = "The schema name to share."
}

variable "tables_to_share" {
  type        = list(string)
  default     = []
  description = "List of tables to share"
}

variable "share_name" {
  description = "Name of share"
  type        = string
}
