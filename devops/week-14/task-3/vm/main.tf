resource "azurerm_virtual_machine" "vm" {
    name                  = "terraform_project_${terraform.workspace}_vm"
    location              = var.location
    resource_group_name   = var.resource_group_name
    network_interface_ids = [var.network_interface_id]
    vm_size               = "Standard_DS1_v2"
    storage_os_disk {
        name              = "terraform_project_${terraform.workspace}_os_disk"
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
        computer_name  = "terraformProject${terraform.workspace}Vm"
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
    delete_data_disks_on_termination = terraform.workspace == "prod" ? false : true
    delete_os_disk_on_termination    = terraform.workspace == "prod" ? false : true
}