
output "admin_username" {
  value = var.admin_username
}

resource "null_resource" "create_ansible_host_inventory" {
  triggers = {
    always_run = "${timestamp()}"
  }

  for_each = {
    prod_1 = azurerm_linux_virtual_machine.prod_server_1.public_ip_address,
    prod_2 = azurerm_linux_virtual_machine.prod_server_2.public_ip_address,
    qa_1   = azurerm_linux_virtual_machine.qa_server_1.public_ip_address
  }
  
  ip_address = each.value

  provisioner "local-exec" {
    command = <<EOT
      echo "[linux_virtual_machines]" > inventory.yml
      echo ${ip_address} >> inventory.yml
      done
    EOT
  }
}