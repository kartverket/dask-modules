output "gcs_bucket_names" {
  value = { for key, mod in module.skyporten_consumer : key => mod.gcs_bucket_name }
}
