# Social Media API - User Authentication

## Setup
1. Install dependencies: `pip install django djangorestframework`
2. Run migrations: `python manage.py migrate`
3. Create superuser: `python manage.py createsuperuser`
4. Start server: `python manage.py runserver`

## API Endpoints
- POST /api/auth/register/ - User registration
- POST /api/auth/login/ - User login
- GET/PUT /api/auth/profile/ - User profile management

## Authentication
The API uses token authentication. Include the token in the Authorization header as "Token <your_token>" for protected endpoints.