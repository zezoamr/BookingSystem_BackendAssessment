# BookingSystem_BackendAssessment

deployment link: http://zezoamr.pythonanywhere.com/api

for documentation: http://zezoamr.pythonanywhere.com/swagger or http://zezoamr.pythonanywhere.com/swagger/?format=openapi

# Booking System API

## Overview

This project is a robust Booking System API built with Django and Django Rest Framework. It provides a comprehensive solution for managing bookings and Zoom meetings, featuring user authentication, meeting creation, booking management, and integration with Zoom API.

## Features

* User registration and authentication
* JWT-based authentication
* Creation and management of Zoom meetings
* Booking creation and management
* Available slots listing
* Email notifications for booking confirmations and cancellations
* Swagger/OpenAPI documentation
* Dockerized application setup

## Tech Stack

* Python
* Django
* Django Rest Framework
* PostgreSQL
* Docker
* Zoom API
* Swagger/OpenAPI

## API Endpoints

* `/api/register/`: User registration
* `/api/login/`: User login (JWT token acquisition)
* `/api/token/refresh/`: Refresh JWT token
* `/api/slots/`: List available booking slots
* `/api/bookings/`: List and create bookings
* `/api/bookings/<int:pk>/`: Retrieve, update, and delete specific bookings
* `/api/zoom/meetings/`: List and create Zoom meetings
* `/api/zoom/meetings/<int:pk>/`: Retrieve and delete specific Zoom meetings

## Setup and Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/booking-system-api.git
    cd booking-system-api
    ```

2. Create a `.env` file in the project root and add the necessary environment variables.

3. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```

4. The API will be available at `http://localhost:8000`.

## API Documentation

The API documentation is available via Swagger UI and ReDoc:

* **Swagger UI**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
* **ReDoc**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## Usage

* Register a new user using the `/api/register/` endpoint.
* Obtain a JWT token by logging in via the `/api/login/` endpoint.
* Use the obtained token in the Authorization header for subsequent requests.
* Create Zoom meetings using the `/api/zoom/meetings/` endpoint.
* List available slots using the `/api/slots/` endpoint.
* Create bookings for available slots using the `/api/bookings/` endpoint.
* Manage your bookings and meetings using the respective endpoints.

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header of your requests:

```http
Authorization: Bearer <your_token_here>
```

## Testing

To run the tests, execute the following command in the Docker container:

```bash
docker-compose run web python manage.py test
```