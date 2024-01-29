resource "azurerm_virtual_network" "vnet" {
    name                = "terraform_project_vnet"
    address_space       = ["10.0.0.0/16"]
    location            = var.location
    resource_group_name = var.resource_group_name
}
    
resource "azurerm_subnet" "subnet" {
    name                 = "terraform_project_subnet"
    resource_group_name  = var.resource_group_name
    virtual_network_name = azurerm_virtual_network.vnet.name
    address_prefixes     = ["10.0.1.0/24"]
}
    
resource "azurerm_public_ip" "publicip" {
    name                         = "terraform_project_public_ip"
    location                     = var.location
    resource_group_name          = var.resource_group_name
    allocation_method            = "Static"
}
    
resource "azurerm_network_security_group" "nsg" {
    name                = "terraform_project_nsg"
    location            = var.location
    resource_group_name = var.resource_group_name
    security_rule {
        name                       = "HTTP"
        priority                   = 103
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "80"
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }
    security_rule {
        name                       = "SSH"
        priority                   = 1001
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "22"
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }
}
    
resource "azurerm_network_interface" "nic" {
    name                      = "terraform_project_nic"
    location                  = var.location
    resource_group_name       = var.resource_group_name
    ip_configuration {
        name                          = "terraform_project_nic_config"
        subnet_id                     = azurerm_subnet.subnet.id
        private_ip_address_allocation = "Dynamic"
        public_ip_address_id          = azurerm_public_ip.publicip.id
    }

}

resource "azurerm_network_interface_security_group_association" "sg_association" {
  network_interface_id      = azurerm_network_interface.nic.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}

output "public_ip_address" {
    value = azurerm_public_ip.publicip.ip_address
}

output "network_interface_id" {
    value = azurerm_network_interface.nic.id
}