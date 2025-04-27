variable "resource_group" {
  description = "Resource group object"
  type        = any
}

variable "container" {
  description = "Container image name"
  type        = string
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
