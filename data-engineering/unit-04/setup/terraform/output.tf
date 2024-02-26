output "username" {
  value = var.local_admin_username
}

output "ipaddress" {
  value = azurerm_public_ip.main.ip_address
}

output "databricks_host" {
  value     = "https://${var.location}.azuredatabricks.net/"
}

output "databricks_token" {
  value     = databricks_token.main.token_value
  sensitive = true
}

resource "local_file" "main" {
  content  = yamlencode({
    "all": {
      "hosts": {
        "${azurerm_public_ip.main.ip_address}": ""
      }
    }
  })
  filename = "${path.module}/../ansible/inventory.yaml"
}