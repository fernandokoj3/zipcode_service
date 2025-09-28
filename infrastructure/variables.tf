#
#  Project environments
#
variable "project_region" {
  description = "Lambda Function region configuration"
  type        = string
  default     = "us-east-1"
}

variable "project_runtime" {
  type    = string
  default = "python3.13"
  #   validation {
  #     condition     = can(regex("^python[3]\\.1([1-9]{1})$", var.project_runtime))
  #     error_message = "This project was configured to python3.11 or above"
  #   }
}

variable "project_handler" {
  description = "Lambda Function entrypoint in your code"
  type        = string
  default     = "app.handler.lambda_handler"
}


variable "project_environments" {
  description = "A map that defines environment variables for the Lambda Function."
  type        = map(string)
  nullable    = false
  default = {
    APP_VERSION  = "1.0.0"
    APP_BASE_URL = "/api/v1"
  }
}

variable "project_base_path" {
  description = "Base path to api gateway"
  type        = string
  default     = "/api/v1"
}

variable "environment" {
  type        = string
  description = "Environment to application deploy"
  default     = "development"
  #   validation {
  #     condition     = contains(["production", "staging", "development"], var.environment)
  #     error_message = "Environment should be one of from production, staging. development"
  #   }
}

variable "file_name" {
  type    = string
  default = "../.build/zipcode_service.zip"
}


variable "log_retention_in_days" {
  description = "The number of days log events are kept in CloudWatch Logs"
  type        = number
  default     = 14
}

variable "vpc_endpoint_id" {
  type    = string
  default = "vpce-<id>>"
}
