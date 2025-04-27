# PLP FINAL DATABASE PROJECT

## Stack
    HTML
    CSS
    JAVASCRIPT
    FASTAPI
## How to get started with the application
- Clone the repository from GitHub:
    - <code> git clone https://github.com/disi98/PLP-FINAL-DATABASE-PROJECT.git</code>

- Create a python environment:
    - <code>python -m venv venv</code>
- Activate the <code>venv</code> virtual env:
    - Windows: <code>./venv/Scripts/activate</code>
    - Linux: <code>source ./venv/bin/Activate </code>
- Install the dependacies
    - From <venv> envoronment: <code>pip insatll -r requirements.txt</code>
- Run the app
## Structure
```bash
# From project root with venv activated
uvicorn main:app --reload
```
 
## API Documentation
Once the server is running, visit:
- http://127.0.0.1:8000/docs for Swagger UI
- http://127.0.0.1:8000/redoc for ReDoc

The available endpoints:

### Users
- **POST /users/** : Create a new user
- **GET /users/** : List users (paginated)
- **DELETE /users/{username}** : Delete a user and associated authors

### Categories
- **POST /categories/** : Create a category
- **GET /categories/** : List categories
- **DELETE /categories/{name}** : Delete a category

### Hashtags
- **POST /hashtags/** : Create a hashtag
- **GET /hashtags/** : List hashtags
- **GET /hashtags/latest** : Get latest 10 hashtags
- **DELETE /hashtags/{id}** : Delete a hashtag

### Authors
- **POST /authors/** : Create an author
- **GET /authors/** : List authors
- **GET /authors/latest** : Get latest 10 authors
- **DELETE /authors/{username}** : Delete an author

### Posts
- **POST /posts/** : Create a post
- **GET /posts/** : List posts
- **GET /posts/latest** : Get latest 10 posts
- **GET /posts/{post_id}** : Retrieve a post
- **PUT /posts/{post_id}** : Update a post
- **DELETE /posts/{post_id}** : Delete a post

## Frontend Dashboard
Open `index.html` in your browser to view the dashboard. Click the buttons to load the latest hashtags, posts, or authors.

## Project Structure
```
├─ main.py           # FastAPI application and CRUD endpoints
├─ index.html        # Frontend dashboard
├─ style.css         # Frontend styling
├─ db_tables.sql     # Database schema and seed data
├─ requirements.txt  # Python dependencies
├─ README.md         # Project documentation
└─ eer_diagram.png    # Entity-relationship diagram
```
