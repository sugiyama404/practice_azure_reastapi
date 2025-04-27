variable "app_name" {
  description = "application name"
  type        = string
  default     = "chatbot"
}

variable "region" {
  description = "AWS region to create resources in"
  type        = string
  default     = "ap-northeast-1"
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

variable "detabase_name" {
  type = string
}
