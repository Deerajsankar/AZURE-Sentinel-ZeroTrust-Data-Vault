resource "azurerm_storage_account" "vault" {
  name                     = "stdeerajvault0007"
  resource_group_name      = azurerm_resource_group.RG.name
  location                 = azurerm_resource_group.RG.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "staging"
  }
}

resource "azurerm_storage_container" "inbound" {
  name                  = "inboundlogs"
  storage_account_id    = azurerm_storage_account.vault.id
  container_access_type = "private"
}