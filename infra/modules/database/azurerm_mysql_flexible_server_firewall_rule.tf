resource "azurerm_mysql_flexible_server_firewall_rule" "mysql" {
  name                = "AllowAllAzureServices"
  resource_group_name = var.resource_group.name
  server_name         = azurerm_mysql_flexible_server.mysql.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
}
