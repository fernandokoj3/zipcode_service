resource "aws_iam_role" "zipcode_lambda_role" {
  name = "${local.context[terraform.workspace].function_name}-role"

  tags = local.tags

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com",
      },
    }],
  })
}

resource "aws_iam_role_policy_attachment" "basic_attachment" {
  policy_arn = aws_iam_policy.zipcode_lambda_policy.arn
  role       = aws_iam_role.zipcode_lambda_role.name
}

resource "aws_iam_policy" "zipcode_lambda_policy" {
  name = "${local.context[terraform.workspace].function_name}-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid = "LogSid"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Sid = "StatementNetSid"
        Action = [
          "ec2:CreateNetworkInterface",
          "ec2:AttachNetworkInterface",
          "ec2:DeleteNetworkInterface",
          "ec2:DescribeNetworkInterfaces"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Sid      = "StatementPvtSid"
        Action   = "execute-api:Invoke"
        Effect   = "Allow"
        Resource = "arn:aws:execute-api:us-east-1:<aws-account-id>:*/*"
      }
    ]
  })
}