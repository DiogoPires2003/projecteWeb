# Web Project - Django Application

## 1. General Information

Course: Web Project  
Academic Year: 2025/2026  
Professors: Roberto Garcia and David Sarrat  

Project repository:  
[url](https://github.com/DiogoPires2003/projecteWeb)

***

### 1.1 Changes from Deliverable 1

- **Environment variables**: `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` are now configured via environment variables (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`) following 12-factor principles.
- **Admin panel**: All models (`Recipe`, `RecipeIngredient`, `SavedRecipe`) are registered in the Django admin interface for easy data management.
- **Form validation**: Recipe create and edit forms now preserve ingredient data on validation errors, and display field-level error messages.
- **Database**: The `db.sqlite3` file is now tracked in git to facilitate testing (as requested in the deliverable).


## 2. E2E Tests

```bash
# Install Playwright browsers (first time)
playwright install chromium

# Run E2E tests
pytest tests_e2e/ -v
```

This project consists of the development of a web application using the Django framework, following the requirements defined in the assignment description.

***

## 3. Data Model

The database used is the same one defined in the first delivery of the project. This decision was made to maintain consistency between phases and to take advantage of a model that had already been previously validated.

The model is composed of several related entities, fulfilling the requirement of including at least three entities with meaningful relationships. Additionally, a coherent and normalized relational structure has been maintained to ensure data integrity.

***

## 4. Authentication System

For user management, Django’s built-in authentication system (`django.contrib.auth`) has been used. This system allows secure handling of user registration and login.

The following functionalities have been implemented:
- User registration
- Login and logout
- Access restriction to certain functionalities based on authentication (for example to add/edit/delete their own recipes the user needs to be identified)

This decision was made to ensure an adequate level of security, avoid implementing unnecessary custom mechanisms, and facilitate integration with the rest of the framework.


***

## 5. User Interface

Regarding the interface, a simple, clear, and functional design has been chosen. The main objective has been to ensure a good user experience and facilitate navigation within the application.

Neutral colors have been used, combined with a primary color to highlight important actions. This choice is based on readability, visual consistency, and accessibility criteria.

***

## 6. Navigation and Data Visualization

Different pages have been developed to allow interaction with the application’s data, such as:
- List pages
- Detail pages
- Home page

These features allow users to explore the information without needing to access the administration panel, thus improving the overall usability of the system.

***

## 7. Administration Panel

The Django administration panel has been enabled to allow efficient data management. Through this panel, it is possible to create, modify, and delete instances of the system’s different entities.

This functionality is especially useful during development and testing, as well as for meeting the project requirements.

***

***

## 8. External API Integration (Web 2.0)

To fulfill the Web 2.0 requirements, the application integrates the **Open Food Facts API**. 

- **Functionality**: When a user is creating or editing a recipe, the system allows them to search for real food products.
- **Implementation**: We use **AJAX (JQuery)** to perform asynchronous requests to the Open Food Facts database without reloading the page.
- **User Assistance**: As the user types an ingredient, the application fetches matching products and displays their nutritional information (like Nutri-Score) to help the user choose the best ingredients for their recipe.

***


## 9. Deployment with Docker

The project includes a configuration based on Docker and docker-compose that allows the application to be run easily and reproducibly.

This decision facilitates deployment across different environments and ensures that the application behaves consistently regardless of the system it runs on.

***

## 10. Best Practices (12-factor)

The application follows the 12-factor app methodology:
- **Codebase**: One codebase tracked in git
- **Dependencies**: Explicitly declared in `requirements.txt`
- **Config**: Configuration via environment variables (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`)
- **Backing services**: SQLite database (swappable via config)
- **Build, release, run**: Docker ensures separation
- **Processes**: Stateless Django application
- **Port binding**: Self-contained via Docker
- **Disposability**: Fast startup and shutdown
- **Dev/prod parity**: Same environment via Docker

***

## 11. Execution Instructions

Prerequisites:
- Docker
- Docker Compose

### 11.1 Configuration

Copy the example environment file and adjust as needed:

```bash
cp .env.example .env
```

### 11.2 Run the application

```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`.

### 11.3 Seed data (optional)

To populate the database with sample recipes:

```bash
docker-compose exec web python seed_recipes.py
```

### 11.4 Admin credentials

Default admin user (create via `createsuperuser`):
- Username: `admin`
- Password: (set during creation)

```bash
docker-compose exec web python manage.py createsuperuser
```

### 11.5 Test users (for E2E tests)

- `us_1` / `TestPass123!`
- `us_2` / `TestPass123!`

***

## 12. GitHub Repository

https://github.com/DiogoPires2003/projecteWeb.git


## 13. Administration Panel Users

In order to access the administration panel, you need to create a superuser.

### 13.1 Administration Panel
- **URL**: `http://localhost:8000/admin`
- **Username**: `admin`
- **Password**: `admin`