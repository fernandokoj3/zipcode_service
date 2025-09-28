resource "aws_security_group" "zipcode_lambda_sg" {
  vpc_id = data.aws_vpc.vpc_main.id
  name   = "${local.context[terraform.workspace].function_name}-lambda-sg"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}