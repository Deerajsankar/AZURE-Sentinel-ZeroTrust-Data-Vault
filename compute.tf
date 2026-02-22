resource "azurerm_service_plan" "compute_plan" {
  name                = "plan-sentinel-compute"
  resource_group_name = azurerm_resource_group.RG.name
  location            = azurerm_resource_group.RG.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "data_engine" {
  name                = "func-deeraj-sentinel-0007"
  resource_group_name = azurerm_resource_group.RG.name
  location            = azurerm_resource_group.RG.location
  service_plan_id     = azurerm_service_plan.compute_plan.id

  storage_account_name       = azurerm_storage_account.vault.name
  storage_account_access_key = azurerm_storage_account.vault.primary_access_key

  site_config {
    application_stack {
      python_version = "3.11"
    }
  }
  identity {
    type = "SystemAssigned"
  }
}