resource "aws_cloudwatch_log_group" "zipcode_api_gw_cw_group" {
  name              = "/aws/lambda/${local.context[terraform.workspace].function_name}"
  retention_in_days = var.log_retention_in_days

  tags_all = local.tags
}

resource "aws_cloudwatch_log_group" "zipcode_lambda_cw_group" {
  name              = "/aws/api-gw/${local.context[terraform.workspace].function_name}"
  retention_in_days = var.log_retention_in_days

  tags_all = local.tags
}