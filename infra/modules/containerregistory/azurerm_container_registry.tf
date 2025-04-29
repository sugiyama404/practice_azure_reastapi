resource "azurerm_container_registry" "main" {
  name                = "mainregistry${random_string.unique_key.result}"
  resource_group_name = var.resource_group.name
  location            = var.resource_group.location
  sku                 = "Basic"
  admin_enabled       = true
}

resource "random_string" "unique_key" {
  length  = 10
  upper   = false
  lower   = true
  numeric = true
  special = false
}
