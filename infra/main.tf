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

resource "azurerm_resource_group" "rg" {
  name     = "${var.app_name}-rg"
  location = "Japan East"
}
