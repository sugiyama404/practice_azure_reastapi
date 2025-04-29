terraform {
  required_version = "=1.10.5"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=4.20"
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
  location = var.location
}

# Resource Providers
module "resource_providers" {
  source = "./modules/resource_providers"

  providers_to_register = [
    "Microsoft.Web",
    "Microsoft.ContainerRegistry"
  ]
}

# Container Registry
module "containerregistry" {
  source         = "./modules/containerregistory"
  resource_group = azurerm_resource_group.resource_group
}

# Bash
module "bash" {
  source                = "./modules/bash"
  image_name            = var.image_name
  registry_name         = module.containerregistry.registry_name
  registry_login_server = module.containerregistry.registry_login_server
}

# Database
module "database" {
  source         = "./modules/database"
  resource_group = azurerm_resource_group.resource_group
  username       = var.username
  password       = var.password
  database_name  = var.database_name
}

# App Service
module "appservice" {
  source                  = "./modules/appservice"
  resource_group          = azurerm_resource_group.resource_group
  image_name              = var.image_name
  username                = var.username
  password                = var.password
  database_name           = var.database_name
  registry_login_server   = module.containerregistry.registry_login_server
  mysql_fqdn              = module.database.mysql_fqdn
  registry_admin_username = module.containerregistry.registry_admin_username
  registry_admin_password = module.containerregistry.registry_admin_password
}
