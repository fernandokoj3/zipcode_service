resource "aws_api_gateway_rest_api" "zipcode_private_api" {
  name        = "${local.context[terraform.workspace].function_name}-pvt"
  description = "Private api gateway for zipcode service"
  tags_all    = local.tags

  endpoint_configuration {
    types = ["PRIVATE"]
  }
}

resource "aws_api_gateway_method" "health_method" {
  rest_api_id   = aws_api_gateway_rest_api.zipcode_private_api.id
  resource_id   = aws_api_gateway_rest_api.zipcode_private_api.root_resource_id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "health_lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.zipcode_private_api.id
  resource_id             = aws_api_gateway_rest_api.zipcode_private_api.root_resource_id
  http_method             = aws_api_gateway_method.health_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.zipcode_lambda.invoke_arn
}

resource "aws_api_gateway_resource" "root_resource_v1" {
  rest_api_id = aws_api_gateway_rest_api.zipcode_private_api.id
  parent_id   = aws_api_gateway_rest_api.zipcode_private_api.root_resource_id
  path_part   = "v1"
}

resource "aws_api_gateway_resource" "v1_zipcode_resource" {
  rest_api_id = aws_api_gateway_rest_api.zipcode_private_api.id
  parent_id   = aws_api_gateway_resource.root_resource_v1.id
  path_part   = "zipcode"
}

resource "aws_api_gateway_resource" "v1_zipcode_resource_param" {
  rest_api_id = aws_api_gateway_rest_api.zipcode_private_api.id
  parent_id   = aws_api_gateway_resource.v1_zipcode_resource.id
  path_part   = "{zipcode}"
}

resource "aws_api_gateway_method" "v1_zipcode_method_param" {
  rest_api_id   = aws_api_gateway_rest_api.zipcode_private_api.id
  resource_id   = aws_api_gateway_resource.v1_zipcode_resource_param.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_zipcode_v1_param_integration" {
  rest_api_id             = aws_api_gateway_rest_api.zipcode_private_api.id
  resource_id             = aws_api_gateway_resource.v1_zipcode_resource_param.id
  http_method             = aws_api_gateway_method.v1_zipcode_method_param.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.zipcode_lambda.invoke_arn
}

resource "aws_api_gateway_deployment" "api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.zipcode_private_api.id
  triggers = {
    redeployment = timestamp()
  }
  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    aws_api_gateway_integration.health_lambda_integration,
    aws_api_gateway_integration.get_zipcode_v1_param_integration
  ]
}

resource "aws_api_gateway_stage" "api_stage" {
  deployment_id = aws_api_gateway_deployment.api_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.zipcode_private_api.id
  stage_name    = local.context[terraform.workspace].stage

}

resource "aws_api_gateway_rest_api_policy" "zipcode_private_api_policy" {
  rest_api_id = aws_api_gateway_rest_api.zipcode_private_api.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Deny"
        Principal = "*"
        Action    = "execute-api:Invoke"
        Resource  = "${aws_api_gateway_rest_api.zipcode_private_api.execution_arn}/*"
        Condition = {
          StringNotEquals = {
            "aws:SourceVpce" = data.aws_vpc_endpoint.vpce_api_gateway.id
          }
        }
      },
      {
        Effect    = "Allow"
        Principal = "*"
        Action    = "execute-api:Invoke"
        Resource  = "${aws_api_gateway_rest_api.zipcode_private_api.execution_arn}/*"
        Condition = {
          "StringEquals" = {
            "aws:SourceVpce" = data.aws_vpc_endpoint.vpce_api_gateway.id
          }
        }
      }
    ]
  })
}
