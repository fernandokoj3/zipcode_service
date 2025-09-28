locals {

  context = {
    development = {
      version       = "1.0.0"
      function_name = "zipcode-service-dev"
      stage         = "dev"
    }

    staging = {
      version       = "1.0.0"
      function_name = "zipcode-service-stg"
      stage         = "stg"
    }

    production = {
      version       = "1.0.0"
      function_name = "zipcode-service"
      stage         = "prd"
    }
  }

  tags = {
    env           = "${terraform.workspace}"
    service       = local.context[terraform.workspace].function_name
    team          = "backend"
    repository    = "zipcode_service"
    documentation = "self"
    created       = "terraform"
  }
}