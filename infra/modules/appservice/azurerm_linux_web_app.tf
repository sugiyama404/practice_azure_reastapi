resource "azurerm_linux_web_app" "main" {
  name                = "mainapp${random_string.unique_key.result}"
  resource_group_name = var.resource_group.name
  location            = var.resource_group.location
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker_image_name        = var.container
      docker_registry_url      = "https://${var.registry_login_server}"
      docker_registry_username = var.registry_admin_username
      docker_registry_password = var.registry_admin_password
    }
  }

  app_settings = {
    "MYSQL_HOST"      = var.mysql_fqdn
    "MYSQL_PORT"      = "3306"
    "MYSQL_USER"      = var.username
    "MYSQL_PASSWORD"  = var.password
    "MYSQL_DATABASE"  = var.database_name
    "MYSQL_SSL"       = "true"
    "STARTUP_COMMAND" = "python main.py"
  }

  lifecycle {
    ignore_changes = [
      site_config[0].application_stack,
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
