# API Documentation


## APIs Overview

- **Base Url**: `127.0.0.1:8000`

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