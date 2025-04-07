terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.54.1"
    }
  }
}

provider "aws" {
  region = var.region
}


resource "aws_instance" "myserver-tf" {
  ami = "ami-016038ae9cc8d9f51"
  instance_type = "t3.nano"

  tags = {
    Name = "SampleServer"
  }
}
