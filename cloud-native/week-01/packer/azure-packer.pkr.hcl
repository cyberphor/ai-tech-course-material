packer {
  required_plugins {
    azure = {
      version = ">= 2.0.2"
      source  = "github.com/hashicorp/azure"
    }
  }
}

source "azure-arm" "main" {
  client_id                         = var.client_id
  managed_image_resource_group_name = var.resource_group
  os_type                           = var.vm_os_type
  image_publisher                   = var.vm_image_publisher
  image_offer                       = var.vm_image_offer
  image_sku                         = var.vm_image_sku
  vm_size                           = var.vm_size
}

build {
  sources = [
    "source.azure-arm.main"
  ]

  #TODO: Copy over all needed files, and run the shell provisioner. Example file provisioner ( how to copy to a VM ):
  provisioner "file" {
    source = "myapp.service"
    destination = "/tmp/myapp.service"
  }

  provisioner "file" {
    source = "run_monolith.sh"
    destination = "/tmp/run_monolith.sh"
  }

  provisioner "shell" {
    environment_vars = [
      #TODO: Add environmental variables here.
    ]
    inline = [
      "cloud-init status --wait",
      #TODO: Add some installation lines here.
      # Copies the temporary monolith to the active directory.
      "cp /tmp/run_monolith.sh .", 
      # Copies the system daemon file to daemon location.
      "sudo mv /tmp/myapp.service /etc/systemd/system/myapp.service", 
      # Makes the monolith run script executable to all
      "sudo chmod +x run_monolith.sh", 
      # Makes the service executable to daemon manager.
      "chmod 644 /etc/systemd/system/myapp.service",
      # Enables daemon to run upon VM start. 
      "sudo systemctl enable myapp.service", 
      "mvn clean package",
    ]
  }
}