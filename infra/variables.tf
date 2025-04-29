variable "app_name" {
  description = "application name"
  type        = string
  default     = "todoapp"
}

variable "location" {
  description = "location"
  type        = string
  default     = "Japan East"
}

variable "image_name" {
  description = "image name"
  type        = string
  default     = "todoflask"
}

variable "subscription_id" {
  type = string
}

variable "username" {
  description = "database username"
  type        = string
}

variable "password" {
  description = "database password"
  type        = string
}

variable "database_name" {
  type = string
}
