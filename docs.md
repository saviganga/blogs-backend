# API Documentation


## APIs Overview

- **Base Url**: `blogs-lb-2023728377.us-east-1.elb.amazonaws.com:8000`

### Authentication
The application uses JWT Authentication for secure access to specific endpoints

#### 1. Admin/Staff Signup
This endpoint allows users to create a new staff account.

- **Endpoint**: `{{BASE_URL}}/users/admins/`
- **Method**: POST

**Request Body:**
```json
{
    "user_name": "ganga-admin",
    "password": "casa1234",
    "re_password": "casa1234"
}
```


#### 2. User Signup
This endpoint allows users to create a new account.

- **Endpoint**: `{{BASE_URL}}/users/account/`
- **Method**: POST

**Request Body:**
```json
{
    "user_name": "ganga",
    "password": "casa1234",
    "re_password": "casa1234"
}
```



#### 3. Admin Login
This endpoint allows admins to login to their accounts.

- **Endpoint**: `{{BASE_URL}}/auth/login/`
- **Method**: POST

**Request Body:**
```json
{
    "username": "jondoe",
    "password": "xxxxxx"
}
```

**Request Headers:**
```json
{
    "entity": "admin"
}
```


#### 4. User Login
This endpoint allows users to login to their accounts.

- **Endpoint**: `{{BASE_URL}}/auth/login/`
- **Method**: POST

**Request Body:**
```json
{
    "username": "jondoe",
    "password": "xxxxxx"
}
```

**Request Headers:**
```json
{
    "entity": "user"
}
```


#### 5. Get admin data
This endpoint allows users to view their staff account information.

- **Endpoint**: `{{BASE_URL}}/users/admins/`
- **Method**: GET
- **Authorization**: true

**Request Headers:**
```json
{
    "Authorization": "JWT {{jwt_token}}"
}
```

#### 6. Get user data
This endpoint allows users to view their user account information.

- **Endpoint**: `{{BASE_URL}}/users/account/`
- **Method**: GET
- **Authorization**: true

**Request Headers:**
```json
{
    "Authorization": "JWT {{jwt_token}}"
}
```


#### 7. Get blog posts
This endpoint allows users to view published blog posts.

- **Endpoint**: `{{BASE_URL}}/blog/posts/`
- **Method**: GET
- **Authorization**: false


#### 8. Get unpublished blog posts
This endpoint allows authors view their unpublished blog posts.

- **Endpoint**: `{{BASE_URL}}/blog/posts/unpublished/`
- **Method**: GET
- **Authorization**: True

**Request Headers:**
```json
{
    "Authorization": "JWT {{jwt_token}}"
}
```

An admin/staff user also has access to this endpoint by passing the the right headers

**Request Headers:**
```json
{
    "Authorization": "JWT {{jwt_token}}",
    "entity": "admin"
}
```


#### 9. Get blog drafts
This endpoint allows authors view the drafts/content history of a particular blog post.

- **Endpoint**: `{{BASE_URL}}/blog/posts/<blogpost_id>/drafts/`
- **Method**: GET
- **Authorization**: True

**Request Headers:**
```json
{
    "Authorization": "JWT {{jwt_token}}"
}
```


#### 10. Create blog post
This endpoint allows authors to create a new blog post. The created content is added to the drafts of the post until it is approved by a staff/admin user.

- **Endpoint**: `{{BASE_URL}}/blog/posts/`
- **Method**: POST
- **Authorization**: True

**Request Body:**
```json
{
    "title": "Newton's First Law of Motion",
    "content": "A body remains at rest or in uniform motion on a straight line except acted upon by an external force",
}
```

**Request Headers:**
```json
{
    "Authorization": "JWT {{jwt_token}}"
}
```


#### 11. Publish blog post
This endpoint allows admins to approve blog post drafts for publishing. Every draft has a unique reference 

- **Endpoint**: `{{BASE_URL}}/blog/posts/<blogpost_id>/publish_draft/`
- **Method**: POST
- **Authorization**: True

**Request Body:**
```json
{
    "reference": "9D7O2I"
}
```

**Request Headers:**
```json
{
    "Authorization": "JWT {{jwt_token}}"
}
```


#### 12. Update blog Post
This endpoint allows authors update the a blog post.

- **Endpoint**: `{{BASE_URL}}/blog/posts/<blogpost_id>/`
- **Method**: PATCH
- **Authorization**: True


**Request Body:**
```json
{
    "content": "For every action, there is an equal and opposite reaction"
}
```

**Request Headers:**
```json
{
    "Authorization": "JWT {{jwt_token}}"
}
```


# Infrastructure and Deployment

## Cloud Infrastructure

The cloud infrastructure for this service is hosted on AWS. Key components include:

- **Containerization**: The application is containerized and runs on AWS Elastic Container Service (ECS) with Fargate. This setup reduces costs associated with virtual machine resource management.
- **Load Balancer**: The ECS cluster is positioned behind an Application Load Balancer (ALB), which restricts access to traffic from the load balancer only, blocking direct public internet access.

## Infrastructure as Code

Terraform is utilized for defining and managing the infrastructure on AWS. The configuration files are located in `./devops/terraform/`:

- **`providers.tf`**: Declares the Terraform providers and defines the backend (AWS S3) for storing the Terraform state.
- **`vars.tf`**: Contains variables used in the Terraform configuration.
- **`security_groups.tf`**: Configures ingress and egress rules for the resources.
- **`alb.tf`**: Provisions the Application Load Balancer, including its target group and listener.
- **`db.tf`**: Sets up the database configuration.
- **`ecs.tf`**: Manages the ECS infrastructure, including the cluster, service, and task definitions.
- **`iam.tf`**: Defines IAM roles and policies for the cloud infrastructure.
- **`vpc.tf`**: Configures and retrieves VPC information.

## Configuration Management

Ansible is used for configuring the application on the provisioned infrastructure. The Ansible script runs from the CI/CD pipeline, ensuring the application is updated with the latest image on every push to the branch.

- **`./devops/ansible/playbooks/update_ecs_task.yaml`**: Updates the AWS ECS task definition and service with the latest application image.

## CI/CD Pipeline

The CI/CD pipeline is built using GitHub Actions.

This setup ensures that application updates are managed efficiently and deployed automatically based on branch activity.
