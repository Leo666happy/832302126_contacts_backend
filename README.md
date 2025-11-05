# Contacts Backend API (FastAPI + Local MySQL)

A lightweight, high-performance contact management backend API built with FastAPI and local MySQL. Supports full CRUD operations, contact search, and avatar uploads—designed for seamless integration with frontend frameworks (Vue/React) in local development.

## Features
- FastAPI-powered with auto-generated interactive docs (no extra setup)
- Local MySQL integration via SQLAlchemy ORM (no cloud dependency)
- Full contact management: Create, Read, Update, Delete & Search
- Avatar upload support with local static file storage
- CORS configured for frontend-backend separation in local environment
- Easy local development with hot-reload

## Tech Stack
| Technology       | Version Requirement | Description                  |
|------------------|---------------------|------------------------------|
| Python           | 3.8+                | Core programming language    |
| FastAPI          | ≥0.120.0            | Backend API framework        |
| Uvicorn          | ≥0.38.0             | ASGI server (hot-reload)     |
| SQLAlchemy       | ≥2.0.0              | ORM for database operations  |
| PyMySQL          | ≥1.0.0              | MySQL database driver        |
| python-dotenv    | ≥1.0.0              | Local environment config     |
| python-multipart | ≥0.0.6              | File upload handling         |

## Project Structure
```
backend/
├── main.py               # API routes & entry point
├── database.py           # Local DB connection setup
├── models.py             # SQLAlchemy ORM models (MySQL tables)
├── schemas.py            # Pydantic data validation
├── crud.py               # CRUD operation logic
├── requirements.txt      # Dependencies list
└── .env                  # Local environment config (not tracked in Git)
```

## Quick Start (Local Development)

### 1. Prerequisites
- Install Python 3.8+ (https://www.python.org/downloads/)
- Install local MySQL 8.0 (https://dev.mysql.com/downloads/mysql/)
- Git (optional, for cloning)

### 2. Clone Repository
```bash
git clone https://github.com/your-username/contacts-project.git
cd contacts-project/backend
```

### 3. Install Dependencies
```bash
# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 4. Local MySQL Setup
1. Start your local MySQL service
2. Create a database via MySQL CLI/Workbench:
   ```sql
   CREATE DATABASE contact_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. Create a `.env` file in the `backend` folder:
   ```env
   # .env file content (update with your local MySQL credentials)
   DATABASE_URL=mysql+pymysql://root:your-local-mysql-password@localhost:3306/contact_db
   PORT=8000
   ```

### 5. Run Local Server
```bash
# Start server with hot-reload (auto-restarts on code changes)
uvicorn main:app --reload
```

### 6. Access API Docs & Test
Open your browser and visit:
- Swagger UI (interactive testing): `http://127.0.0.1:8000/docs`
- ReDoc (API documentation): `http://127.0.0.1:8000/redoc`

All endpoints are testable directly in the Swagger UI—no extra tools needed!

## API Endpoints
| Endpoint               | Method | Description                  | Parameters                          |
|------------------------|--------|------------------------------|-------------------------------------|
| `/api/contacts`        | GET    | Get all contacts             | `skip` (pagination start), `limit`  |
| `/api/contacts/search` | GET    | Search contacts (name/phone) | `keyword` (search term)             |
| `/api/contacts/{id}`   | GET    | Get single contact by ID     | `id` (path parameter)               |
| `/api/contacts`        | POST   | Create new contact           | Form data + optional avatar file    |
| `/api/contacts/{id}`   | PUT    | Update existing contact      | `id` (path) + form data/avatar      |
| `/api/contacts/{id}`   | DELETE | Delete contact               | `id` (path parameter)               |

## Notes
- The `static/avatars` folder will be auto-created to store uploaded avatars
- Local MySQL credentials are stored in `.env` (never commit this file to Git)
- For frontend integration: Use `http://localhost:8000/api` as the base URL
