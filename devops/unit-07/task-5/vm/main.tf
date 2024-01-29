resource "azurerm_virtual_machine" "vm" {
    name                  = "terraform_project_vm"
    location              = var.location
    resource_group_name   = var.resource_group_name
    network_interface_ids = [var.network_interface_id]
    vm_size               = "Standard_DS1_v2"
    storage_os_disk {
        name              = "terraform_project_os_disk"
        caching           = "ReadWrite"
        create_option     = "FromImage"
        managed_disk_type = "Premium_LRS"
    }
    storage_image_reference {
        publisher = "Canonical"
        offer     = "UbuntuServer"
        sku       = "16.04.0-LTS"
        version   = "latest"
    }
    os_profile {
        computer_name  = "terraformProjectVm"
        admin_username = var.admin_username
        admin_password = var.admin_password
    }
    os_profile_linux_config {
        disable_password_authentication = false
    }
    provisioner "remote-exec" {
        connection {
            type = "ssh"
            user = var.admin_username
            password = var.admin_password
            host = var.public_ip_address
        }
        inline = [
            "sudo apt-get -y update",
            "sudo apt-get -y install apache2",
            "echo Welcome to the cloud course! | sudo tee /var/www/html/index.html"
        ]
    }
}

resource "azurerm_monitor_action_group" "action_group" {
  name                = "terraform_project_action_group"
  resource_group_name = var.resource_group_name
  short_name          = "devopsadmin"
  email_receiver {
    name          = "sendtodevopsadmin"
    email_address = "vf@andrew.cmu.edu"
  }
}

resource "azurerm_monitor_metric_alert" "alert" {
  name = "terraform_project_alert_cpu"
  resource_group_name = var.resource_group_name
  scopes = [azurerm_virtual_machine.vm.id]
  description = "An alert to watch the metric Percentage CPU"
  enabled = true
  criteria {
    metric_namespace = "Microsoft.Compute/virtualMachines"
    metric_name = "Percentage CPU"
    operator    = "GreaterThan"
    threshold   = 2
    aggregation = "Average"
  }
  action {
      action_group_id = azurerm_monitor_action_group.action_group.id
  }
}