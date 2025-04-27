resource "azurerm_mysql_flexible_server" "mysql" {
  name                = "mysql"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku_name            = "B_Standard_B1ms"

  administrator_login    = var.mysql_username
  administrator_password = var.mysql_password

  version = "8.0.21"

  lifecycle {
    ignore_changes = [
      administrator_login,
      administrator_password,
      zone
    ]
  }
}
