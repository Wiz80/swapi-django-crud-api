# main.tf

# Provider configuration for AWS
provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = "us-east-1"
}

# Create a key pair for SWAPI project
resource "aws_key_pair" "swapi_ssh_key" {
  key_name   = "swapi_ssh_key_pair"
  public_key = file("~/.ssh/id_rsa.pub")
}

# Security group for SWAPI EC2 instance
resource "aws_security_group" "swapi_allow_ssh" {
  name_prefix = "swapi_allow_ssh_"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 instance running Ubuntu for SWAPI project
resource "aws_instance" "swapi_ubuntu_instance" {
  ami           = "ami-0dba2cb6798deb6d8"  # Ubuntu Server 22.04 LTS en us-east-1 (Free Tier Eligible)
  instance_type = "t2.micro"
  key_name      = aws_key_pair.swapi_ssh_key.key_name

  vpc_security_group_ids = [aws_security_group.swapi_allow_ssh.id]

  tags = {
    Name = "SwapiUbuntuInstance"
  }

  # Provisioning to run Ansible playbook after instance creation
  provisioner "local-exec" {
    command = <<EOT
      ansible-playbook -i ${self.public_ip}, -u ubuntu --private-key ~/.ssh/id_rsa Ansible/install-docker.yaml
    EOT
  }
}
