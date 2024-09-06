
# get the vpc fom aws account
data "aws_vpcs" "current_vpcs" {}

# get the subnets in the vpc
data "aws_subnets" "available_subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpcs.current_vpcs.ids[0]]
  }
}

resource "aws_db_subnet_group" "sensor_data_subnet_group" {
  name       = "${var.PROJECT_NAME}_subnet_group"
  subnet_ids = data.aws_subnets.available_subnets.ids

  tags = {
    Name = "${var.PROJECT_NAME}_subnet_group"
  }
}