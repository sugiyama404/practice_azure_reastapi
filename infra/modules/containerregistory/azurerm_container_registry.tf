resource "azurerm_container_registry" "acr" {
  name                = "${replace(var.project, "-", "")}${var.environment}acr"
  resource_group_name = var.resource_group.name
  location            = var.resource_group.location
  sku                 = "Basic"
  admin_enabled       = true
}
