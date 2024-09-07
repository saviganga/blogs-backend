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


#### 5. Get user data
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