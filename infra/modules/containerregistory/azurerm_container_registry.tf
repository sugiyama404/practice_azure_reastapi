resource "azurerm_container_registry" "main" {
  name                = "mainregistry"
  resource_group_name = var.resource_group.name
  location            = var.resource_group.location
  sku                 = "Basic"
  admin_enabled       = true
}
