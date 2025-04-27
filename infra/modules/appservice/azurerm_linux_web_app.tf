resource "azurerm_linux_web_app" "app" {
  name                = "${var.project}-${var.environment}-app"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.asp.id

  site_config {
    application_stack {
      # docker_image_name = "nginx"
      # docker_registry_url = "https://index.docker.io"
      docker_image_name        = var.container
      docker_registry_url      = "https://${azurerm_container_registry.acr.login_server}"
      docker_registry_username = azurerm_container_registry.acr.admin_username
      docker_registry_password = azurerm_container_registry.acr.admin_password
    }
  }

  app_settings = {
    "MYSQL_HOST"     = azurerm_mysql_flexible_server.mysql.fqdn
    "MYSQL_PORT"     = "3306"
    "MYSQL_USER"     = var.mysql_username
    "MYSQL_PASSWORD" = var.mysql_password
    "MYSQL_DATABASE" = var.mysql_database
    "MYSQL_SSL"      = "true"
  }

  lifecycle {
    ignore_changes = [
      site_config[0].application_stack,
    ]
  }
}
