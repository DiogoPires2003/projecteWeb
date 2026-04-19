# Web Project - Django Application

## 1. General Information

Course: Web Project  
Academic Year: 2025/2026  
Professors: Roberto Garcia and David Sarrat  

Project repository:  
https://github.com/DiogoPires2003/projecteWeb.git  

This project consists of the development of a web application using the Django framework, following the requirements defined in the assignment description.

***

## 2. Data Model

The database used is the same one defined in the first delivery of the project. This decision was made to maintain consistency between phases and to take advantage of a model that had already been previously validated.

The model is composed of several related entities, fulfilling the requirement of including at least three entities with meaningful relationships. Additionally, a coherent and normalized relational structure has been maintained to ensure data integrity.

***

## 3. Authentication System

For user management, Django’s built-in authentication system (`django.contrib.auth`) has been used. This system allows secure handling of user registration and login.

The following functionalities have been implemented:
- User registration
- Login and logout
- Access restriction to certain functionalities based on authentication

This decision was made to ensure an adequate level of security, avoid implementing unnecessary custom mechanisms, and facilitate integration with the rest of the framework.

***

## 4. User Interface

Regarding the interface, a simple, clear, and functional design has been chosen. The main objective has been to ensure a good user experience and facilitate navigation within the application.

Neutral colors have been used, combined with a primary color to highlight important actions. This choice is based on readability, visual consistency, and accessibility criteria.

***

## 5. Navigation and Data Visualization

Different pages have been developed to allow interaction with the application’s data, such as:
- List pages
- Detail pages
- Home page

These features allow users to explore the information without needing to access the administration panel, thus improving the overall usability of the system.

***

## 6. Administration Panel

The Django administration panel has been enabled to allow efficient data management. Through this panel, it is possible to create, modify, and delete instances of the system’s different entities.

This functionality is especially useful during development and testing, as well as for meeting the project requirements.

***

## 7. Deployment with Docker

The project includes a configuration based on Docker and docker-compose that allows the application to be run easily and reproducibly.

This decision facilitates deployment across different environments and ensures that the application behaves consistently regardless of the system it runs on.

***

## 8. Best Practices (12-factor)

As much as possible, development has followed the recommendations of the 12-factor app methodology, especially in aspects such as:
- Separation between configuration and code
- Use of environment variables
- Ease of deployment

This approach improves the maintainability and scalability of the application.

***

## 9. Execution Instructions

Prerequisites:
- Docker
- Docker Compose

To run the application, execute the following command:

```bash
docker-compose up --build
```

Fuentes
