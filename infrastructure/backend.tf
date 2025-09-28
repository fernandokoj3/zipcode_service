terraform {
  backend "s3" {
    bucket         = "<replace>-tfstate"
    key            = "<replace>/zipcode_service/lambda/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform_state_lock"
  }
}
