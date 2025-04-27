output "registry_login_server" {
  value       = azurerm_container_registry.main.login_server
  description = "The login server of the Container Registry"
}
