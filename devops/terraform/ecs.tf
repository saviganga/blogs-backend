resource "aws_ecs_cluster" "ecs-cluster" {
  name = "${var.PROJECT_NAME}-ecs-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  depends_on = [
    aws_db_instance.sensor_data_db_instance
  ]
}

resource "aws_ecs_task_definition" "ecs_task_definition" {
  family                   = "${var.PROJECT_NAME}-family"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  
  container_definitions = jsonencode([
    {
      name      = var.CONTAINER_NAME
      image     = var.CONTAINER_IMAGE
      essential = true
      portMappings = [
        {
          containerPort = var.CONTAINER_PORT
          hostPort      = var.HOST_PORT
          protocol      = "tcp"
        }
      ]
      environment = [
        {
          name  = "SECRET_KEY"
          value = var.SECRET_KEY
        },
        {
          name  = "ENVIRONMENT"
          value = var.ENVIRONMENT
        },
        {
          name  = "POSTGRES_HOST"
          value = aws_db_instance.sensor_data_db_instance.address
        },
        {
          name  = "POSTGRES_USER"
          value = aws_db_instance.sensor_data_db_instance.username
        },
        {
          name  = "POSTGRES_PASSWORD"
          value = var.DB_PASSWORD
        },
        {
          name  = "POSTGRES_DB"
          value = aws_db_instance.sensor_data_db_instance.db_name
        },
        {
          name  = "POSTGRES_PORT"
          value = tostring(aws_db_instance.sensor_data_db_instance.port)
        }
      ]
      logConfiguration = {
            logDriver = "awslogs"
            options = {
            "awslogs-create-group" = "true"
            "awslogs-group"         = "/ecs/${var.PROJECT_NAME}"
            "awslogs-region"        = var.REGION
            "awslogs-stream-prefix" = "ecs"
            }
        }
    }
  ])

  runtime_platform {
    operating_system_family = var.ECS_TASK_OS_FAMILY
    cpu_architecture        = var.ECS_TASK_CPU_ARCHITECTURE
  }

  depends_on = [
    aws_db_instance.sensor_data_db_instance
  ]

}

resource "aws_ecs_service" "ecs_service" {
  name            = "${var.PROJECT_NAME}-ecs-service"
  cluster         = aws_ecs_cluster.ecs-cluster.id
  task_definition = aws_ecs_task_definition.ecs_task_definition.arn
  desired_count   = 2

  network_configuration {
    subnets          = data.aws_subnets.available_subnets.ids
    security_groups  = [aws_security_group.app_sg.id]
    assign_public_ip = true
  }

  force_new_deployment = true

  lifecycle {
    ignore_changes = [
      task_definition
    ]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.tg-ecs-task.arn
    container_name   = var.CONTAINER_NAME
    container_port   = var.CONTAINER_PORT
  }
    deployment_minimum_healthy_percent = 50
    deployment_maximum_percent         = 200

   launch_type                        = "FARGATE"
   scheduling_strategy                = "REPLICA"

   depends_on = [
    aws_db_instance.sensor_data_db_instance
  ]

}