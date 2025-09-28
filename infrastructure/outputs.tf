output "vpce_dns_name" {
  value = format(
    "https://%s/%s",
    data.aws_vpc_endpoint.vpce_api_gateway.dns_entry[0].dns_name,
    local.context[terraform.workspace].stage
  )
}

output "api_gateway_id" {
  value = format(
    "%s / %s",
    aws_api_gateway_rest_api.zipcode_private_api.id,
    local.context[terraform.workspace].stage
  )
}