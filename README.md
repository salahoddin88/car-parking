# Nearest Car Parking Finder
## Overview
The Nearest Car Parking Finder is a web application developed in Python using Django and Django Rest Framework. It is designed to assist users in finding the closest available car parking based on their current location (latitude and longitude). The system not only identifies the nearest parking spaces but also considers the remaining time of existing parked cars to ensure efficiency and convenience.

## Key Features
- Location-Based Searching: Users can input their current latitude and longitude coordinates to find nearby parking options.
- Real-Time Availability: The system calculates the availability of parking spots based on the remaining time of cars currently parked in those spaces.
- Scalable and Efficient: Developed using Django and Django Rest Framework, the application is highly scalable and can handle a large number of users and parking spots.
- User-Friendly Interface: The user interface is intuitive and easy to use, making it simple for users to locate the most convenient parking spot.

## Technologies Used
- Python: The core programming language used for the backend logic and algorithms.
- Django: The web framework that powers the application, providing a robust structure for development.
- Django Rest Framework: Used for creating RESTful APIs to handle data exchange between the frontend and backend.
- Docker: The application is containerized using Docker, making it portable and easy to manage.
- PostgreSQL: The database management system used to efficiently store and manage data.

## How it Works
- Users provide their current latitude and longitude coordinates with radius in kilometer
- The system calculates the available parking spaces within the vicinity.
- Availability is determined based on the remaining time of cars currently parked in each spot.
- Users are presented with a list of the nearest and most convenient parking options.

## Future Enhancements
This project can be further improved by adding features like:
- User registration and authentication for a personalized experience.
- Reserve parking sport
