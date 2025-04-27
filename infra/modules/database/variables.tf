variable "project" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
}

variable "resource_group" {
  description = "Resource group object"
  type        = any
}

variable "mysql_username" {
  description = "MySQL admin username"
  type        = string
}

variable "mysql_password" {
  description = "MySQL admin password"
  type        = string
  sensitive   = true
}

variable "mysql_database" {
  description = "MySQL database name"
  type        = string
}
