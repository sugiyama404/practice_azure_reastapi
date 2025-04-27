resource "azurerm_linux_web_app" "main" {
  name                = "main"
  resource_group_name = var.resource_group.name
  location            = var.resource_group.location
  service_plan_id     = azurerm_service_plan.asp.id

  site_config {
    application_stack {
      docker_image_name        = var.container
      docker_registry_url      = "https://${module.containerregistry.acr.login_server}"
      docker_registry_username = module.containerregistry.acr.admin_username
      docker_registry_password = module.containerregistry.acr.admin_password
    }
  }

  app_settings = {
    "MYSQL_HOST"     = module.database.mysql.fqdn
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
