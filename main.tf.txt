resource "azurerm_resource_group" "RG" {
  name     = "RG-DEERAJ"
  location = "Central India"

  tags = {
    Environment = "Lab"
    Project     = "Sentinel-Vault"
    Owner       = "Deeraj"
  }
}

resource "azurerm_network_security_group" "nsg" {
  name                = "deeraj-nsg-secure"
  location            = azurerm_resource_group.RG.location
  resource_group_name = azurerm_resource_group.RG.name

  tags = {
    Environment = "Lab"
    Project     = "Sentinel-Vault"
    Owner       = "Deeraj"
  }
}

resource "azurerm_virtual_network" "vnet" {
  name                = "deeraj-vnet"
  location            = azurerm_resource_group.RG.location
  resource_group_name = azurerm_resource_group.RG.name
  address_space       = ["10.0.0.0/16"]

  tags = {
    Environment = "Lab"
    Project     = "Sentinel-Vault"
    Owner       = "Deeraj"
  }
}

resource "azurerm_subnet" "snet" {
  name                 = "deeraj-subnett"
  resource_group_name  = azurerm_resource_group.RG.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}