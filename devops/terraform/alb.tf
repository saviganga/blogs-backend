resource "aws_lb" "lb" {
  name               = "${var.PROJECT_NAME}-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.elb_sg.id]
  subnets            = data.aws_subnets.available_subnets.ids

  enable_deletion_protection = false

  tags = {
    Name = "${var.PROJECT_NAME}-lb"
  }

  depends_on = [
    aws_db_instance.sensor_data_db_instance
  ]
}


# create a target group for the load balancer
resource "aws_lb_target_group" "tg-ecs-task" {
  name        = "${var.PROJECT_NAME}-tg"
  port        = var.CONTAINER_PORT
  protocol    = var.ALB_TARGET_GROUP_PROTOCOL
  vpc_id      = data.aws_vpcs.current_vpcs.ids[0]
  target_type = var.ALB_TARGET_GROUP_TARGET_TYPE

  health_check {
    path = var.ALB_TARGET_GROUP_HEALTH_CHECK_PATH
  }

}



# Create an ALB listener to handle load balancer redirect # port that connects to the internet and sends request to the tg
resource "aws_lb_listener" "alb-listener" {
  load_balancer_arn = aws_lb.lb.arn
  port              = var.HOST_PORT
  protocol          = var.ALB_LISTENER_PROTOCOL

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg-ecs-task.arn
  }
}


# print out some output
output "lb_hostname_output" {
  value = aws_lb.lb.dns_name
}
