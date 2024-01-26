packer {
  required_plugins {
    azure = {
      version = ">= 2.0.2"
      source  = "github.com/hashicorp/azure"
    }
  }
}

source "azure-arm" "main" {
  tenant_id                         = var.tenant_id           # defined and set in variables.pkr.hcl
  subscription_id                   = var.subscription_id     # defined and set in variables.pkr.hcl
  client_id                         = var.client_id           # defined in variables.pkr.hcl and set in secret.pkrvars.hcl      
  client_secret                     = var.client_secret       # defined in variables.pkr.hcl and set in secret.pkrvars.hcl
  location                          = var.location            # defined and set in variables.pkr.hcl
  managed_image_resource_group_name = var.resource_group_name # defined and set in variables.pkr.hcl
  managed_image_name                = var.managed_image_name  # defined and set in variables.pkr.hcl
  os_type                           = var.vm_os_type          # defined and set in variables.pkr.hcl
  image_publisher                   = var.vm_image_publisher  # defined and set in variables.pkr.hcl
  image_offer                       = var.vm_image_offer      # defined and set in variables.pkr.hcl
  image_sku                         = var.vm_image_sku        # defined and set in variables.pkr.hcl
  vm_size                           = var.vm_size             # defined and set in variables.pkr.hcl
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
      # these environment variable are needed for "mvn clean package" to work
      # they are also in "run_monolith.sh" because the cloudchat Java app depends on them
      "MYSQL_HOST=${var.mysql_host}",                      # defined and set in variables.pkr.hcl
      "MYSQL_USER=${var.mysql_user}",                      # defined in variables.pkr.hcl and set in secret.pkrvars.hcl
      "MYSQL_PASSWORD=${var.mysql_password}",              # defined in variables.pkr.hcl and set in secret.pkrvars.hcl
      "SPRING_REDIS_HOST=${var.spring_redis_host}",        # defined and set in variables.pkr.hcl
      "SPRING_REDIS_PORT=${var.spring_redis_port}",        # defined and set in variables.pkr.hcl
      "SPRING_REDIS_PASSWORD=${var.spring_redis_password}" # defined in variables.pkr.hcl and set in secret.pkrvars.hcl
    ]
    inline = [
      "cloud-init status --wait",
      "chmod +x run_monolith.sh",                                   # Makes the monolith run script executable to all
      "chmod 644 myapp.service",                                    # Makes the service executable to daemon manager
      "sudo apt update",                                            #TODO: Add some installation lines here
      "sudo apt install -y maven openjdk-17-jdk openjdk-17-jre jq", #TODO: Add some installation lines here
      "sudo cp myapp.service /etc/systemd/system/myapp.service",    # Copies the system daemon file to daemon location
      "sudo systemctl enable myapp.service",                        # Enables daemon to run upon VM start
      "mvn clean package"                                           #TODO: Add Maven build sequence here 
    ]
  }
}