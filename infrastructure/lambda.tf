resource "aws_lambda_function" "zipcode_lambda" {
  function_name = local.context[terraform.workspace].function_name
  filename      = var.file_name
  description   = "Integration on zipcode brokers"
  runtime       = var.project_runtime
  handler       = var.project_handler
  timeout       = 30
  memory_size   = 256

  vpc_config {
    subnet_ids         = data.aws_subnets.private.ids
    security_group_ids = [aws_security_group.zipcode_lambda_sg.id]
  }

  source_code_hash = filebase64sha256(var.file_name)


  tags_all = local.tags

  lifecycle {
    ignore_changes = []
  }

  environment {
    variables = merge(
      var.project_environments, {

      }
    )
  }

  role = aws_iam_role.zipcode_lambda_role.arn
}


resource "aws_lambda_permission" "api_permission_network_create" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.zipcode_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.zipcode_private_api.execution_arn}/*/*"
}