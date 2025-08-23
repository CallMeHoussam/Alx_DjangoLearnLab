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
## Posts and Comments API Endpoints

### Posts
- `GET /api/posts/` - List all posts (paginated)
- `POST /api/posts/` - Create a new post (authenticated)
- `GET /api/posts/{id}/` - Retrieve a specific post
- `PUT /api/posts/{id}/` - Update a post (owner only)
- `PATCH /api/posts/{id}/` - Partial update (owner only)
- `DELETE /api/posts/{id}/` - Delete a post (owner only)
- `POST /api/posts/{id}/comment/` - Add comment to post (authenticated)
- `GET /api/posts/{id}/comments/` - List comments for a post

### Comments
- `GET /api/comments/` - List all comments
- `POST /api/comments/` - Create a new comment (authenticated)
- `GET /api/comments/{id}/` - Retrieve a specific comment
- `PUT /api/comments/{id}/` - Update a comment (owner only)
- `PATCH /api/comments/{id}/` - Partial update (owner only)
- `DELETE /api/comments/{id}/` - Delete a comment (owner only)

### Filtering and Search
- Search posts: `/api/posts/?search=keyword`
- Order posts: `/api/posts/?ordering=created_at` or `/?ordering=-created_at`
- Pagination: All list endpoints are paginated with page size of 10

### Example Requests
**Create Post:**
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "This is my first post content"}'