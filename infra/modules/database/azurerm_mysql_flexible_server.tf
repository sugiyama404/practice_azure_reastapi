resource "azurerm_mysql_flexible_server" "mysql" {
  name                = "${var.resource_group.name}-mysql-${random_string.unique_key.result}"
  resource_group_name = var.resource_group.name
  location            = var.resource_group.location
  sku_name            = "B_Standard_B1ms"

  administrator_login    = var.username
  administrator_password = var.password

  version = "8.0.21"

  lifecycle {
    ignore_changes = [
      administrator_login,
      administrator_password,
      zone
    ]
  }
}

resource "random_string" "unique_key" {
  length  = 10
  upper   = false
  lower   = true
  numeric = true
  special = false
}
