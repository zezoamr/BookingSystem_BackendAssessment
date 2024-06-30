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
   <pre><div class="relative flex flex-col rounded-lg"><div class="text-text-300 absolute pl-3 pt-2.5 text-xs"></div><div class="pointer-events-none sticky z-20 my-0.5 ml-0.5 flex items-center justify-end px-1.5 py-1 mix-blend-luminosity top-0"><div class="from-bg-300/90 to-bg-300/70 pointer-events-auto rounded-md bg-gradient-to-b p-0.5 backdrop-blur-md"></div></div></div></pre>
