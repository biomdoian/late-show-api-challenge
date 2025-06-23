# Flask Code Challenge — Late Show API
The Late Show API is a Flask-based RESTful service for managing talk show guests, episodes, and appearances with JWT-based user authentication.
## Setup Instructions
Steps to set up the PostgreSQL database, install Python dependencies, and configure environment variables for the API.

## PostgreSQL Database Setup
1. Create the Database:

sudo -u postgres createdb late_show_db

2. Set Password for postgres User:
Enter the PostgreSQL shell as the postgres system user and set a password:

sudo -u postgres psql
ALTER USER postgres WITH PASSWORD 'your_postgres_password';
\q

3. Install Python Dependencies
Navigate to your project's root directory and install all required packages using Pipenv:

cd ~/development/code/code-challenges/late-show-api-challenge/
pipenv install flask flask_sqlalchemy flask_migrate flask-jwt-extended psycopg2-binary SQLAlchemy-serializer Faker Flask-Bcrypt python-dotenv flask-restful
pipenv shell

4. Configure Environment Variables (.env)
Create a file named .env inside the server/ directory.

server/.env content:

DATABASE_URI="postgresql://postgres:your_postgres_password@localhost:5432/late_show_db"
FLASK_SECRET_KEY='your_generated_flask_secret_key_here'
JWT_SECRET_KEY='your_generated_jwt_secret_key_here'

Replace your_postgres_password with your actual PostgreSQL password.

5. Generate FLASK_SECRET_KEY (24 bytes) and JWT_SECRET_KEY (32 bytes) by running:

python -c 'import os; print(os.urandom(24).decode("latin-1"))'

python -c 'import os; print(os.urandom(32).decode("latin-1"))'
Copy the output string and paste it into the .env file.

### How to Run
Follow these steps to initialize the database, seed data, and start the Flask API.

1. Navigate to the server/ directory:

cd ~/development/code/code-challenges/late-show-api-challenge/server

2. Set the Flask application entry point:

export FLASK_APP=app.py

3. Run Database Migrations:

flask db init # Only run once for initial setup
flask db migrate -m "Initial migration"
flask db upgrade head

4. Seed the Database with Sample Data:

python seed.py

5. Start the Flask Application:

python app.py

The API will run on http://127.0.0.1:5555/.

# Authentication Flow
The API uses JWT for authentication.

>. Register: POST /register to create a user with a username and password.

>. Login: POST /login with username and password to receive an access_token.

>. Token Usage: For protected routes, include the access_token in the Authorization header as Bearer <token>.

Route List + Sample Request/Response
All routes operate on http://127.0.0.1:5555/.

1. POST /register
Description: Creates a new user account.

Auth Required?: No

Sample Request:

 POST http://127.0.0.1:5555/register
Content-Type: application/json

{
    "username": "new_user_name",
    "password": "your_secure_password"
}

Sample Response: HTTP/1.1 201 Created

{
    "message": "User registered successfully"
}
. POST /login
Description: Authenticates a user and returns a JWT token.

Auth Required?: No

Sample Request:

POST http://127.0.0.1:5555/login
Content-Type: application/json

{
    "username": "testuser",
    "password": "password123"
}

Sample Response: HTTP/1.1 200 OK

{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2U..."
}

2. GET /episodes
Description: Lists all episodes.

Auth Required?: No

Sample Request:

GET http://127.0.0.1:5555/episodes

Sample Response: HTTP/1.1 200 OK

[
    {"id": 1, "date": "2023-06-23", "number": 1, ...},
    {"id": 2, "date": "2023-06-30", "number": 2, ...}
]

GET /episodes/<int:id>
Description: Retrieves a specific episode by ID, including its appearances.

Auth Required?: No

Sample Request:

GET http://127.0.0.1:5555/episodes/1

Sample Response: HTTP/1.1 200 OK

{
    "id": 1, "date": "2023-06-23", "number": 1,
    "appearances": [
        {"id": 5, "rating": 4, "guest_id": 10, "episode_id": 1, "guest": {"id": 10, "name": "Jane Smith", ...}},
        ...
    ]
}

3. DELETE /episodes/<int:id>
Description: Deletes an episode and its associated appearances.

Auth Required?: Yes

Sample Request:

DELETE http://127.0.0.1:5555/episodes/2
Authorization: Bearer <your_access_token_here>

Sample Response: HTTP/1.1 204 No Content (Empty body)

GET /guests
Description: Lists all guests.

Auth Required?: No

Sample Request:

GET http://127.0.0.1:5555/guests

Sample Response: HTTP/1.1 200 OK

[
    {"id": 1, "name": "Dr. Susan Miller", "occupation": "Psychologist", ...},
    {"id": 2, "name": "Mr. John Doe", "occupation": "Engineer", ...}
]

POST /appearances
Description: Creates a new appearance record.

Auth Required?: Yes

Sample Request:

POST http://127.0.0.1:5555/appearances
Content-Type: application/json
Authorization: Bearer <your_access_token_here>

{
    "guest_id": 1,
    "episode_id": 5,
    "rating": 4
}

Sample Response: HTTP/1.1 201 Created

{
    "id": 101, "rating": 4, "guest_id": 1, "episode_id": 5, ...
}

# Postman Usage Guide
A Postman Collection named challenge-4-lateshow.postman_collection.json is provided in the root of this repository to test the API.

Import the Collection:

Open Postman, click "Import", select "File", and choose challenge-4-lateshow.postman_collection.json.

### Set Up Environment for JWT:

Click the "No Environment" dropdown in Postman (top-right). Select "Add new environment" and name it Late Show API Dev.

Ensure Late Show API Dev is selected.

Run the "Login User" request (under "Auth" folder). Its script automatically saves the access_token to your active environment.

Run Requests: Use the imported requests. Protected routes (like POST /appearances and DELETE /episodes/<int:id>) will automatically use the access_token from your environment.

GitHub Repository Link
https://github.com/biomdoian/late-show-api-challenge.git