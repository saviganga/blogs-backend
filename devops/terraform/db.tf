resource "aws_db_instance" "sensor_data_db_instance" {
  identifier             = "${var.PROJECT_NAME}-rds"
  db_name                = var.DB_NAME
  instance_class         = var.DB_INSTANCE_CLASS
  allocated_storage      = var.DB_ALOCATED_STORAGE
  engine                 = var.DB_ENGINE
  engine_version         = var.DB_ENGINE_VERSION
  username               = var.DB_USER
  password               = var.DB_PASSWORD
  db_subnet_group_name   = aws_db_subnet_group.sensor_data_subnet_group.name
  vpc_security_group_ids = [aws_security_group.sensor_data_rds_sg.id]
  parameter_group_name   = aws_db_parameter_group.sensor_data_db_parameter_group.name
  publicly_accessible    = true
  skip_final_snapshot    = true
  deletion_protection    = false


}

resource "aws_db_parameter_group" "sensor_data_db_parameter_group" {
  name   = "${var.PROJECT_NAME}-parameter-group"
  family = "postgres16"

  parameter {
    name  = "log_connections"
    value = "1"
  }
}


# print out some output
output "db_hostname_output" {
  value = aws_db_instance.sensor_data_db_instance.address
}
