variable "REGION" {
  default = "us-east-1"
}

variable "PROJECT_NAME" {
  type    = string
  default = "blogs"

}

variable "DB_PASSWORD" {
  type        = string
  description = "database password"
  sensitive   = true
}

variable "DB_USER" {
  type        = string
  description = "database user"
}

variable "DB_NAME" {
  type    = string
  default = "blogs"
}

variable "DB_ENGINE" {
  type    = string
  default = "postgres"
}

variable "DB_ENGINE_VERSION" {
  type    = string
  default = "16.1"
}

variable "DB_ALOCATED_STORAGE" {
  type    = number
  default = 5
}


variable "DB_INSTANCE_CLASS" {
  type    = string
  default = "db.t3.micro"
}

variable "HOST_PORT" {
  type    = number
  default = 8000
}


variable "ALB_TARGET_GROUP_PROTOCOL" {
  type    = string
  default = "HTTP"
}


variable "ALB_TARGET_GROUP_TARGET_TYPE" {
  type    = string
  default = "ip"
}


variable "ALB_TARGET_GROUP_HEALTH_CHECK_PATH" {
  type    = string
  default = "/blog/posts/health/"
}

variable "ALB_LISTENER_PROTOCOL" {
  type    = string
  default = "HTTP"
}


variable "ECS_TASK_OS_FAMILY" {
  type    = string
  default = "LINUX"
}

variable "ECS_TASK_CPU_ARCHITECTURE" {
  type    = string
  default = "X86_64"
}


variable "EXECUTION_ROLE_ARN" {
  type    = string
}


variable "CONTAINER_PORT" {
  type    = number
  default = 8000

}


variable "CONTAINER_NAME" {
  type    = string
  default = "blogs-api"

}


variable "CONTAINER_IMAGE" {
  type    = string
  default = "saviganga/blogs:20240906185508"

}


variable "UPTRACE_DSN" {
  type    = string
  default = "https://_6cA0PMdKqG1CIaQ7tPzrw@api.uptrace.dev?grpc=4317"

}


variable "POSTGRES_PORT" {
  type    = string
  default = "5432"

}


variable "ENVIRONMENT" {
  type    = string
  default = "CLOUD"

}


variable "SECRET_KEY" {
  type    = string

}

