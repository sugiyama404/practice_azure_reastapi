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

variable "username" {
  description = "Cognito username"
  type        = string
}

variable "password" {
  description = "Cognito password"
  type        = string
}
