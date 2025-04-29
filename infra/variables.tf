variable "app_name" {
  description = "application name"
  type        = string
  default     = "chatbot"
}

variable "subscription_id" {
  type = string
}

variable "container" {
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
