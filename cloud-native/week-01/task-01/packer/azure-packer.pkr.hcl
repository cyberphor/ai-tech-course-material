packer {
  required_plugins {
    azure = {
      version = ">= 2.0.2"
      source  = "github.com/hashicorp/azure"
    }
  }
}

source "azure-arm" "main" {
  tenant_id                         = var.tenant_id
  subscription_id                   = var.subscription_id
  client_id                         = var.client_id
  client_secret                     = var.client_secret
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
    source      = "../README.md"
    destination = "/home/packer/README.md"
  }

  provisioner "file" {
    source      = "../pom.xml"
    destination = "/home/packer/pom.xml"
  }

  provisioner "file" {
    source      = "../src"
    destination = "/home/packer/src"
  }

  provisioner "file" {
    source      = "run_monolith.sh"
    destination = "/home/packer/run_monolith.sh"
  }

  provisioner "file" {
    source      = "myapp.service"
    destination = "/home/packer/myapp.service"
  }

  provisioner "shell" {
    environment_vars = [
      # these environment variable are needed for the "mvn clean package" sentence below
      # they were also added to the "run_monolith.sh" file when the app is ran
      "MYSQL_HOST=${var.mysql_host}",
      "MYSQL_USER=${var.mysql_user}",
      "MYSQL_PASSWORD=${var.mysql_password}",
      "SPRING_REDIS_HOST=${var.spring_redis_host}",
      "SPRING_REDIS_PORT=${var.spring_redis_port}",
      "SPRING_REDIS_PASSWORD=${var.spring_redis_password}"
    ]
    inline = [
      "cloud-init status --wait",
      "chmod +x run_monolith.sh",                                   # Makes the monolith run script executable to all
      "chmod 644 myapp.service",                                    # Makes the service executable to daemon manager
      "sudo apt update",                                            #TODO: Add some installation lines here
      "sudo apt install -y maven openjdk-17-jdk openjdk-17-jre jq", #TODO: Add some installation lines here
      "sudo cp myapp.service /etc/systemd/system/myapp.service",    # Copies the system daemon file to daemon location
      "sudo systemctl enable myapp.service",                        # Enables daemon to run upon VM start
      "mvn clean package",                                          #TODO: Add Maven build sequence here 
      "./run_monolith.sh"
    ]
  }
}