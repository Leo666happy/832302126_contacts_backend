# Contacts Backend API (FastAPI)

A lightweight, high-performance contact management backend API built with FastAPI—supports CRUD operations, contact search, and avatar uploads for seamless frontend (Vue/React) integration in local development.

## Features
- FastAPI-powered with auto-generated interactive docs
- Full contact management: Create, Read, Update, Delete & Search
- Avatar upload support (auto-creates `static/avatars` storage)
- CORS configured for frontend-backend separation
- Hot-reload for easy local development

## Tech Stack
| Technology       | Version Requirement | Description                  |
|------------------|---------------------|------------------------------|
| Python           | 3.8+                | Core language                |
| FastAPI          | ≥0.120.0            | API framework                |
| Uvicorn          | ≥0.38.0             | ASGI server (hot-reload)     |
| SQLAlchemy       | ≥2.0.0              | ORM for database operations  |
| PyMySQL          | ≥1.0.0              | MySQL driver                 |
| python-dotenv    | ≥1.0.0              | Environment config           |
| python-multipart | ≥0.0.6              | File upload handling         |

## Project Structure
```
backend/
├── main.py               # API routes & entry point
├── database.py           # DB connection setup
├── models.py             # ORM models (MySQL tables)
├── schemas.py            # Pydantic data validation
├── crud.py               # CRUD logic
├── requirements.txt      # Dependencies
└── .env                  # Local config (not tracked in Git)
```

## Quick Start (Local Development)

### 1. Prerequisites
- Python 3.8+ (https://www.python.org/downloads/)
- Local MySQL 8.0 (https://dev.mysql.com/downloads/mysql/)
- Git (optional)

### 2. Clone & Setup
```bash
# Clone repo (or download .zip)
git clone https://github.com/your-username/contacts-project.git
cd contacts-project/backend

# Create/activate virtual environment
python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure .env file (add MySQL credentials)
echo "DATABASE_URL=mysql+pymysql://root:your-password@localhost:3306/contact_db" > .env
echo "PORT=8000" >> .env
```

### 3. Run Server
```bash
# Start with hot-reload
uvicorn main:app --reload
```

### 4. Access API Docs
Test endpoints directly via interactive docs:
- Swagger UI: `http://127.0.0.1:8000/docs` (recommended)
- ReDoc: `http://127.0.0.1:8000/redoc`

## Core API Endpoints
| Endpoint               | Method | Description                  | Parameters                          |
|------------------------|--------|------------------------------|-------------------------------------|
| `/api/contacts`        | GET    | Get all contacts             | `skip` (pagination), `limit`        |
| `/api/contacts/search` | GET    | Search (name/phone)          | `keyword` (search term)             |
| `/api/contacts/{id}`   | GET    | Get single contact           | `id` (path parameter)               |
| `/api/contacts`        | POST   | Create contact               | Form data + optional avatar         |
| `/api/contacts/{id}`   | PUT    | Update contact               | `id` + form data/avatar             |
| `/api/contacts/{id}`   | DELETE | Delete contact               | `id` (path parameter)               |

## Notes
- Create MySQL database `contact_db` before running (see MySQL docs)
- Store MySQL credentials in `.env` (never commit to Git)
- Frontend base URL: `http://localhost:8000/api`
