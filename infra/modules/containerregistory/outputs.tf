output "registry_login_server" {
  value       = azurerm_container_registry.main.login_server
  description = "The login server of the Container Registry"
}

output "registry_admin_username" {
  value       = azurerm_container_registry.main.admin_username
  description = "The admin username of the Container Registry"
}

output "registry_admin_password" {
  value       = azurerm_container_registry.main.admin_password
  description = "The admin password of the Container Registry"
}

output "registry_name" {
  value       = azurerm_container_registry.main.name
  description = "The name of the Container Registry"
}
