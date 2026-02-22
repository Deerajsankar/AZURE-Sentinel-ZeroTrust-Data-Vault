resource "azurerm_role_assignment" "data_contributor" {
  scope                = azurerm_storage_account.vault.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = "7a897306-fc50-43b5-8513-7cb35cd20280"
}
resource "azurerm_role_assignment" "function_data_access" {
  scope                = azurerm_storage_account.vault.id
  role_definition_name = "Storage Blob Data Contributor"

  # This dynamically grabs the ID of the badge Azure just printed!
  principal_id = azurerm_linux_function_app.data_engine.identity[0].principal_id
}