# blogs-backend

## Setup

### Prerequisites

To run the development environment, you need to have the following installed:

- **Django**
- **Docker**
- **Docker Compose**
- **Environment Variables**

### Environment Variables

A `.env.example` file has been added to the repository. You should create a `.env` file and fill in the required fields with your values to configure your environment. The `ENVIRONMENT` field has been prefilled to suit the configurations on the application.

## Run the project

1. Clone the repository
```bash
git clone git@github.com:saviganga/blogs-backend.git
```

2. Set up your `.env` file
```bash
cd blogs-backend/
cp ./blogs-backend/.env.example ./blogs-backend/.env
```
Fill the .env file with your values

3. Build the project using `docker-compose`
```bash
docker-compose build
```

4. Test connectivity by making a GET request on postman on this endpont `http://127.0.0.1:8000/sensors/sensor-data/health/' or running this command in a new terminal
```bash
curl http://127.0.0.1:8000/blog/posts/health/

# response
{"status":"SUCCESS","message":"Success"}
```


5. After the build is completed, start the project with `docker-compose`
```bash
docker-compose up
```

6. Run database migrations: To complete the setup, run the database migrations. In another terminal tab, while your app is still runnung, run the following command
```bash
docker exec -it blogs-backend python3 manage.py migrate
```