variable "resource_group" {
  description = "Resource group object"
  type        = any
}

variable "username" {
  description = "MySQL admin username"
  type        = string
}

variable "password" {
  description = "MySQL admin password"
  type        = string
  sensitive   = true
}

variable "database_name" {
  description = "MySQL database name"
  type        = string
}
