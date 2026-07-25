# Parcel Locker - Full-Stack Web Application

A comprehensive, containerized full-stack web application built with a modern tech stack. The project features a robust Python/Flask backend and a dynamic React/TypeScript frontend, fully orchestrated using Docker. 

This repository serves as a showcase of scalable architecture, secure API design (JWT authentication), and modern deployment practices.

## Tech Stack

**Frontend:**
* React 19 & TypeScript
* Vite (Build Tool)
* TailwindCSS 4 (Styling)
* React Router 7 (Routing)
* Axios (HTTP Client)

**Backend:**
* Python (3.14+)
* Flask & Flask-RESTful (API Framework)
* SQLAlchemy & Flask-Migrate (ORM & Database Migrations)
* PyJWT (Authentication)
* Gunicorn (WSGI HTTP Server)

**Infrastructure & DevOps:**
* Docker & Docker Compose
* Nginx (Reverse Proxy)
* MySQL (Relational Database)

## Architecture

The application is fully containerized and consists of four main services:
1. **`frontend-nginx`**: Serves the application and acts as a reverse proxy (Port: `80`).
2. **`frontend-react`**: Vite development server for the frontend (Port: `5173`).
3. **`backend-flask`**: Flask API running securely behind Gunicorn (Port: `8000`).
4. **`mysql-backend`**: MySQL database with persistent volume storage (Port: `3307`).

## ⚙️ Local Development Setup

### Prerequisites
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

## 1. Clone the repository
```bash
git clone https://github.com/PawelBaniusiewicz/Simple-Parcel-Locker.git
cd Simple-Parcel-Locker
```

## 2. Environment Configuration
The project requires environment variables for both the frontend and backend. Example files are provided.

**Backend Configuration:**
Create a .env file in the backend directory based on the example:
```bash
cp backend/.env.example backend/.env
```
Note: Make sure to fill in the JWT secrets and Mail configuration in the newly created .env file.


**Frontend Configuration:**
Create a .env file in the frontend directory based on the example:
```bash
cp frontend/.env.example frontend/.env
```

## 3. Alternative A: Running Locally with uv (Backend Development)
If you prefer to run or develop the Flask backend natively on your machine using uv instead of Docker:
#### 1. Navigate to the backend directory:
```bash
cd backend
```

#### 2. Synchronize dependencies (this will automatically create a .venv virtual environment and install all required packages):
```bash
uv sync
```

#### 3. Configure your IDE (e.g., PyCharm / VS Code) to use the newly created virtual environment located at backend/.venv/bin/python or backend/.venv/Scripts/python as the project interpreter.

## 4. Docker Configuration
Rename the example Docker Compose file to activate it:
```bash
cp docker-compose.yml.example docker-compose.yml
```

## 5. Build and Run
Start the entire stack using Docker Compose:
```bash
docker compose up -d --build
```

## 6. Database Initialization (Migrations)
Before fully using the application, you must apply the database migrations to create the necessary tables in the MySQL database. Since the backend runs inside a Docker container, you need to execute the migration commands from within it.

**Step-by-step approach:**
1. List all running containers to find the exact name of your backend container (look for the one running the Flask API):
```bash
docker ps
```
2. Access the backend container's interactive shell (replace <backend_container_name> with the actual name from the previous step):
```bash
docker exec -it <container_id or container_name> bash
```

3. Initialize the migrations directory (using --app main to specify the entry point):
```bash
flask --app main db init
```

4. Generate the initial migration script based on your ORM models:
```bash
flask --app main db migrate -m "Initial migration"
```

5. Apply the migration to create the tables in the database:
```bash
flask --app main db upgrade
```

6. Type `exit` to leave the container shell.

## 💡 Quick Alternative:
If you know your backend service name in the docker-compose.yml file (e.g., backend-flask), you can run these commands directly from your host machine without entering the interactive shell sequentially:
```bash
docker compose exec <container_name> flask --app main db init
docker compose exec <container_name> flask --app main db migrate -m "Initial migration"
docker compose exec <container_name> flask --app main db upgrade
```

**The services will be available at:**
* Frontend Application (Nginx): http://localhost:80
* Frontend Development Server: http://localhost:5173
* Backend API: http://localhost:8000/api
* Database: localhost:3307

**Key Features (Backend)**
* RESTful API architecture.
* Secure user authentication and authorization using JSON Web Tokens (JWT).
* Email integration for account activation and notifications (flask-mail).
* Data validation and serialization using Pydantic (flask-pydantic).
* Cross-Origin Resource Sharing (CORS) configured for secure client-server communication.

Created by Paweł Baniusiewicz