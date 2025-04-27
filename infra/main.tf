terraform {
  required_version = "=1.10.5"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=4.0"
    }
  }
}

provider "azurerm" {
  resource_provider_registrations = "none"
  subscription_id                 = var.subscription_id
  features {}
}

resource "azurerm_resource_group" "resource_group" {
  name     = "${var.app_name}-rg"
  location = "Japan East"
}

# Container Registry
module "containerregistry" {
  source         = "./modules/containerregistory"
  resource_group = azurerm_resource_group.resource_group
}

# Database
module "database" {
  source         = "./modules/database"
  project        = var.app_name
  environment    = terraform.workspace
  resource_group = azurerm_resource_group.resource_group
  username       = var.username
  password       = var.password
  detabase_name  = var.detabase_name
}

# App Service
module "appservice" {
  source                = "./modules/appservice"
  resource_group        = azurerm_resource_group.resource_group
  container             = var.container
  username              = var.username
  password              = var.password
  detabase_name         = var.detabase_name
  registry_login_server = module.containerregistry.registry_login_server
  mysql_fqdn            = module.database.mysql.fqdn
}
