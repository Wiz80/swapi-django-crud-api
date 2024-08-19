# swapi-django-crud-api

## Project Description

This project consists of a CRUD API built with Django that interacts with the SWAPI (Star Wars API). The goal is to allow querying, storing, and manipulating data from the SWAPI API in a local PostgreSQL database (The project is configured to use any Database) and then expose that data through a RESTful API.

The project includes configurations to deploy the application on a server with Docker, and it also uses infrastructure as code with Terraform to provision an EC2 instance on AWS and Ansible to automate the installation of Docker on the instance.

## API Endpoints

The project includes the following endpoints for performing CRUD operations on the `Planet` model:

1. **Store data from graphql SWAPI API**:
   - **Endpoint**: `/api/v1/query-store/`
   - **Method**: POST
   - **Description**: Store data from SWAPI API all planets 
     ```

2. **Create a Planet**:
   - **Endpoint**: `/api/v1/planets/create/`
   - **Method**: POST
   - **Description**: Allows creating a new planet record.
   - **Request Body**:
     ```json
     {
       "name": "Tatooine",
       "population": "200000",
       "terrains": "desert",
       "climates": "arid"
     }
     ```

3. **List Planets**:
   - **Endpoint**: `/api/v1/planets/`
   - **Method**: GET
   - **Description**: Returns a list of all stored planets.

4. **Retrieve a Planet's Details**:
   - **Endpoint**: `/api/v1/planets/<id>/`
   - **Method**: GET
   - **Description**: Returns details of a specific planet based on its ID.

5. **Update a Planet**:
   - **Endpoint**: `/api/v1/planets/<id>/update/`
   - **Method**: PUT or PATCH
   - **Description**: Allows updating a specific planet's data.

6. **Delete a Planet**:
   - **Endpoint**: `/api/v1/planets/<id>/delete/`
   - **Method**: DELETE
   - **Description**: Deletes a specific planet.

## Project Installation and Configuration

### Prerequisites

- Python 3.10+
- Docker and Docker Compose
- Terraform and Ansible (for AWS deployment)

### Local Setup

1. Clone the repository:
   ```bash
   git clone git@github.com:Wiz80/swapi-django-crud-api.git
   cd swapi-django-crud-api
   ```
2. Create and activate a virtual environment:
  ```bash
   python -m venv venv
   source venv/bin/activate
```

3. Install the dependencies:
  ```bash
   pip install -r requirements.txt
  ```

4.Set up the `.env` file with your database credentials:
  ```bash
  DB_ENGINE=django.db.backends.postgresql
  DB_USER=swapi
  DB_NAME=swapi-user
  DB_PASSWORD=your_password
  DB_HOST=localhost
  DB_PORT=5432
 ```

5. Apply the database migrations:
  ```bash
  python manage.py migrate
  ```
6. Create a superuser for accessing the Django admin panel:
  ```bash
  python manage.py createsuperuser
  ```
7. Start the Django development server:
  ```bash
  python manage.py runserver
  ```
## Unit Testing
The project includes a set of unit tests for each of the CRUD endpoints. The tests are implemented using pytest and pytest-django.

To run the tests, use the following command:
```bash
  pytest request_swapi/tests.py   
  ```
The tests cover the following cases:

* Creating planets.
* Retrieving specific planets.
* Listing planets.
* Updating planets.
* Deleting planets.
* Handling null values in the population, terrains, and climates fields.

## Production Deployment with Docker
The project is dockerized and can be deployed using Docker Compose. The services include:
* Django application.
* PostgreSQL.
* Nginx to serve the application.
  
### Steps to Deploy with Docker:
Build the images and start the containers:
1. The project is dockerized and can be deployed using Docker Compose. The services include:
 ```bash
  docker-compose up --build -d
 ```

This project has a bash script that wait until the creation of the database container and then apply the migrations and create a superuser trough a command of Django:
entrypoint.sh
```bash
  #!/bin/bash
  
  # Wait until database is ready
  echo "Waiting for PostgreSQL to start..."
  while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
  done
  echo "PostgreSQL started"
  
  # Exec migrations
  python manage.py migrate
  
  # Create the superuser using the custom command
  python manage.py create_superuser
  
  # Init Gunicorn
  exec "$@"

 ```
## Infrastructure as Code with Terraform and Ansible
The project uses Terraform to provision infrastructure on AWS, which includes:

* An EC2 instance running Ubuntu.
* A security group that allows traffic on ports 22 (SSH), 80 (HTTP), and 8000 (Django).
* Ansible is used to install Docker and Docker Compose on the EC2 instance.
### Steps to Provision Infrastructure
1. Set up environment variables for your AWS credentials:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
```
2. Initialize Terraform:

```bash
terraform init
```
3. Review the Terraform execution plan:
```bash
terraform plan
```
4. Apply the Terraform plan to provision the infrastructure:
```bash
terraform apply
```
This will deploy the EC2 instance on AWS, install Docker and Docker Compose using Ansible, and open the necessary ports.

## Using the Endpoints from the EC2 Instance
Once the EC2 instance is configured and running, you can access the API endpoints directly using the public IP address of the instance. In this case, the public IP address is 18.234.245.235.

## Using SWAPI Postman Workspace
You could go to this workspace that I made in order to test from postman the endpoints built
`https://web.postman.co/workspace/SWAPI-Django-Project~a2660101-5741-4e2b-9020-3c86b9d6d748/collection/19176433-a4cdfbb6-c9ac-4d70-9011-60b8c3fbb9c4`

Example of making requests to the endpoints:
1. List Planets:

```bash
curl http://18.234.245.235/api/v1/planets/
```

2. Create a Planet:

```bash
curl -X POST http://18.234.245.235/api/v1/planets/create/ -H "Content-Type: application/json" -d '{"name": "Naboo", "population": "450000", "terrains": "grassy hills", "climates": "temperate"}'
```

3. Update a Planet:
```bash
curl -X PUT http://18.234.245.235/api/v1/planets/1/update/ -H "Content-Type: application/json" -d '{"name": "Tatooine", "population": "200000", "terrains": "desert", "climates": "arid"}'
```

4. Delete a Planet:

```bash
curl -X DELETE http://18.234.245.235/api/v1/planets/1/delete/
```
# Conclusion
This project implements a Django CRUD API to interact with data from the SWAPI API. The infrastructure is configured using Terraform and Ansible for deployment on AWS, and Docker is used for portability and production deployment. With this setup, you can run the application both locally and in a production environment in the cloud.
