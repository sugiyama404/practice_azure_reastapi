resource "azurerm_service_plan" "main" {
  name                = "main-asp"
  resource_group_name = var.resource_group.name
  location            = var.resource_group.location
  os_type             = "Linux"
  sku_name            = "B1"
}
