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
  location                          = var.location
  managed_image_resource_group_name = var.resource_group
  managed_image_name                = var.managed_image_name
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
      "sudo apt update",                                              #TODO: Add some installation lines here.
      "sudo apt install -y maven openjdk-17-jdk openjdk-17-jre jq",   #TODO: Add some installation lines here.
      "cp /tmp/run_monolith.sh .",                                    # Copies the temporary monolith to the active directory.
      "sudo mv /tmp/myapp.service /etc/systemd/system/myapp.service", # Copies the system daemon file to daemon location.
      "sudo chmod +x run_monolith.sh",                                # Makes the monolith run script executable to all
      "chmod 644 /etc/systemd/system/myapp.service",                  # Makes the service executable to daemon manager.
      "sudo systemctl enable myapp.service",                          # Enables daemon to run upon VM start. 
      "mvn clean package",                                            #TODO: Add Maven build sequence here. 
    ]
  }
}