resource "azurerm_mysql_flexible_database" "mysql" {
  name                = var.database_name
  resource_group_name = var.resource_group.name
  server_name         = azurerm_mysql_flexible_server.mysql.name
  charset             = "utf8mb4"
  collation           = "utf8mb4_unicode_ci"
}
