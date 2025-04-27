terraform {
  required_version = "=1.10.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# IAM
module "iam" {
  source   = "./modules/iam"
  app_name = var.app_name
}

# Lambda
module "lambda" {
  source                                  = "./modules/lambda"
  app_name                                = var.app_name
  lambda_authorizer_iam_role_arn          = module.iam.lambda_authorizer_iam_role_arn
  apigatewayv2_api_http_api_execution_arn = module.apigateway.apigatewayv2_api_http_api_execution_arn
}

# API Gateway
module "apigateway" {
  source                               = "./modules/apigateway"
  app_name                             = var.app_name
  lambda_protected_endpoint_invoke_arn = module.lambda.lambda_protected_endpoint_invoke_arn
  cognito_user_pool_client_id          = module.cognito.cognito_user_pool_client_id
  cognito_user_pool_main_endpoint      = module.cognito.cognito_user_pool_main_endpoint
}

# Cognito
module "cognito" {
  source   = "./modules/cognito"
  username = var.username
  password = var.password
}
