
resource "aws_security_group" "elb_sg" {
  name        = "${var.PROJECT_NAME}-elb-sg"
  description = "Allow TLS inbound traffic from the internet"

  ingress {
    description = "Allow TLS inbound traffic from the internet"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow TLS inbound traffic from the internet"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }


  ingress {
    description = "Allow TLS inbound traffic from the internet"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "${var.PROJECT_NAME}-elb-sg"
  }
}

# provision security groups
resource "aws_security_group" "sensor_data_rds_sg" { # allow only the load balancer ?
  name        = "${var.PROJECT_NAME}_sensor_data_rds_sg"
  description = "Allow TLS inbound traffic from the internet to port 5432"

  ingress {
    description = "Allow all inbound traffic to port 5432"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "${var.PROJECT_NAME}_sensor_data_rds_sg"
  }
}


resource "aws_security_group" "app_sg" {
  name        = "${var.PROJECT_NAME}-app-sg"
  description = "Allow TLS inbound traffic from the elb security group"

  ingress {
    from_port       = var.CONTAINER_PORT
    to_port         = var.CONTAINER_PORT
    protocol        = "tcp"
    security_groups = [aws_security_group.elb_sg.id]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "${var.PROJECT_NAME}-app-sg"
  }
}


output "sensor_data_rds_sg_output" {
  value = aws_security_group.sensor_data_rds_sg.name
}

