
output "admin_username" {
  value = var.admin_username
}

resource "null_resource" "create_ansible_host_group_prod" {
  triggers = {
    always_run = "${timestamp()}"
  }
  
  provisioner "local-exec" {
    command = "echo [${var.ansible_host_group_prod}] > ${var.ansible_inventory_file_path}"
  }
}

resource "null_resource" "update_ansible_host_group_prod" {
  triggers = {
    always_run = "${timestamp()}"
  }

  for_each = {
    prod1 = azurerm_linux_virtual_machine.prod_server_1.public_ip_address,
    prod2 = azurerm_linux_virtual_machine.prod_server_2.public_ip_address,
  }

  provisioner "local-exec" {
    command = "echo ${each.value} >> ${var.ansible_inventory_file_path}"
  }
}

resource "null_resource" "create_ansible_host_group_qa" {
  triggers = {
    always_run = "${timestamp()}"
  }
  
  provisioner "local-exec" {
    command = <<-EOF
      echo "" >> ${var.ansible_inventory_file_path}
      echo [${var.ansible_host_group_qa}] >> ${var.ansible_inventory_file_path}
    EOF
  }
}

resource "null_resource" "update_ansible_host_group_qa" {
  triggers = {
    always_run = "${timestamp()}"
  }

  for_each = {
    qa3 = azurerm_linux_virtual_machine.qa_server_1.public_ip_address
  }

  provisioner "local-exec" {
    command = "echo ${each.value} >> ${var.ansible_inventory_file_path}"
  }
}