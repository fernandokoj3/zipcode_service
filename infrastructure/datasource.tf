data "aws_vpc" "vpc_main" {
  tags = {
    Name = "<vpc-production-replace>"
  }
}


data "aws_subnets" "public" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.vpc_main.id]
  }

  filter {
    name   = "availability-zone"
    values = ["us-east-1a", "us-east-1b", "us-east-1c"]
  }

  tags = {
    tier = "public"
  }
}


data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.vpc_main.id]
  }

  filter {
    name   = "availability-zone"
    values = ["us-east-1a", "us-east-1b", "us-east-1c"]
  }

  tags = {
    tier = "private"
  }
}

data "aws_vpc_endpoint" "vpce_api_gateway" {
  id = var.vpc_endpoint_id
}