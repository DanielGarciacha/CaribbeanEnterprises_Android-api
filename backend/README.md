# Caribbean Enterprises - Backend API

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)

A modern, secure REST API built with FastAPI for the Caribbean Enterprises mobile application. Provides authentication, user management, and role-based access control.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [API Endpoints](#api-endpoints)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Server](#running-the-server)
- [Testing](#testing)
- [Deployment](#deployment)
- [Project Structure](#project-structure)

## Overview

The Caribbean Enterprises backend is a RESTful API service that handles user authentication, authorization, and data management for the mobile application. It implements JWT-based authentication with role-based access control supporting three user types: Normal Users, Business Owners, and Administrators.

### Key Features

- Secure JWT authentication
- Role-based access control (RBAC)
- Password hashing with bcrypt
- MySQL database with SQLAlchemy ORM
- Interactive API documentation (Swagger/ReDoc)
- CORS enabled for mobile app integration
- Comprehensive error handling
- Environment-based configuration

## Features

### Authentication & Security
- JWT (JSON Web Tokens) for stateless authentication
- Secure password hashing using bcrypt
- Token-based session management
- Configurable token expiration
- Protected endpoints with Bearer authentication

### User Management
- User registration with validation
- Email uniqueness validation
- Username uniqueness validation
- User profile retrieval
- Role assignment (normal, empresario, admin)

### Role-Based Access Control
Three user roles with different access levels:
- **Normal**: Standard user access
- **Empresario**: Business owner with additional features
- **Admin**: Full platform access and management

### API Documentation
- Interactive Swagger UI at `/docs`
- Alternative ReDoc documentation at `/redoc`
- Complete endpoint specifications
- Request/response examples
- Authentication flow documentation

### Database Management
- MySQL relational database
- SQLAlchemy ORM for type-safe queries
- Connection pooling
- Automatic schema migrations
- Test data generation scripts

## Technology Stack

### Core Framework
- **FastAPI** 0.115.5 - Modern, fast web framework
- **Uvicorn** 0.34.0 - Lightning-fast ASGI server
- **Python** 3.8+ - Programming language

### Database
- **MySQL** 8.0+ - Relational database
- **SQLAlchemy** 2.0.36 - SQL toolkit and ORM
- **PyMySQL** 1.1.1 - Pure Python MySQL driver

### Security & Authentication
- **python-jose** 3.3.0 - JWT implementation
- **passlib** 1.7.4 - Password hashing library
- **cryptography** 44.0.0 - Cryptographic recipes

### Data Validation
- **Pydantic** 2.10.3 - Data validation using Python type annotations
- **email-validator** 2.2.0 - Email validation

### Utilities
- **python-dotenv** 1.0.1 - Environment variable management
- **python-multipart** 0.0.18 - Multipart form data support

## Architecture

The backend follows a modular, layered architecture:

```
┌─────────────────────────────────────┐
│      Presentation Layer             │
│   (API Routers, Endpoints)          │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│      Business Logic Layer           │
│   (Authentication, Validation)      │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│      Data Access Layer              │
│   (Repositories, ORM Models)        │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│      Database Layer                 │
│   (MySQL Database)                  │
└─────────────────────────────────────┘
```

### Design Patterns
- **Repository Pattern** - Data access abstraction
- **Dependency Injection** - FastAPI's built-in DI
- **DTO Pattern** - Pydantic models for data transfer
- **Factory Pattern** - Database session creation

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Authentication Endpoints

#### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@test.com",
    "role": "admin",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

#### Register
```http
POST /auth/register
Content-Type: application/json

{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "securepass123"
}
```

**Response:** Same as login (auto-login after registration)

#### Get Profile
```http
GET /auth/profile
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@test.com",
  "role": "admin",
  "created_at": "2024-01-01T00:00:00"
}
```

### Health Check Endpoints

#### Root
```http
GET /
```

**Response:**
```json
{
  "message": "CTP Authentication API",
  "version": "1.0.0",
  "status": "active",
  "docs": "/docs"
}
```

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "ctp-api"
}
```

## Installation

### Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)
- XAMPP (recommended for Windows) or standalone MySQL

### Step 1: Environment Setup

Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Copy the example environment file:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=ctp_db

# Security Configuration
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | MySQL host address | localhost |
| `DB_PORT` | MySQL port | 3306 |
| `DB_USER` | Database username | root |
| `DB_PASSWORD` | Database password | (empty) |
| `DB_NAME` | Database name | ctp_db |
| `SECRET_KEY` | JWT signing key | (must set) |
| `ALGORITHM` | JWT algorithm | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime | 1440 (24h) |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |

### Security Best Practices

1. **Change the SECRET_KEY**: Generate a secure random key
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **Use strong database passwords** in production

3. **Configure CORS** properly for production:
   ```python
   # In main.py
   allow_origins=["https://your-domain.com"]  # Specific origins only
   ```

4. **Enable HTTPS** in production environments

5. **Set appropriate token expiration** based on security requirements

## Database Setup

### Option 1: Using XAMPP (Windows)

1. Start XAMPP Control Panel
2. Start MySQL service
3. Open phpMyAdmin (http://localhost/phpmyadmin)
4. Create database:
   - Click "New"
   - Database name: `ctp_db`
   - Collation: `utf8mb4_unicode_ci`
   - Click "Create"

### Option 2: MySQL Command Line

```sql
CREATE DATABASE ctp_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Option 3: Using Scripts

#### Windows
```bash
# Double-click or run:
scripts\init_db\init_database.bat
```

#### Command Line
```bash
python scripts/init_db/init_db.py
```

### Database Schema

The initialization script creates the following table:

#### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role ENUM('normal', 'admin', 'empresario') DEFAULT 'normal' NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    INDEX idx_username (username),
    INDEX idx_email (email)
);
```

### Test Data

The initialization script creates three test users:

| Username | Email | Password | Role |
|----------|-------|----------|------|
| admin | admin@test.com | admin123 | admin |
| empresario | empresario@test.com | empresario123 | empresario |
| usuario | usuario@test.com | usuario123 | normal |

## Running the Server

### Development Mode

#### Option 1: Using Scripts (Windows)
```bash
# Double-click or run:
scripts\start_server\start_server.bat
```

#### Option 2: Using Uvicorn Directly
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Option 3: Using Python Module
```bash
python -m uvicorn main:app --reload
```

#### Option 4: Running main.py
```bash
python main.py
```

The server will start and be available at:
- API: http://localhost:8000
- Swagger Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc

### Production Mode

For production, use Gunicorn with Uvicorn workers:

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Configuration options:
- `-w 4`: Number of worker processes (adjust based on CPU cores)
- `-k uvicorn.workers.UvicornWorker`: Use Uvicorn worker class
- `--bind 0.0.0.0:8000`: Bind to all interfaces on port 8000

## Testing

### Manual Testing with Swagger

1. Start the server
2. Open http://localhost:8000/docs
3. Test endpoints interactively

### Testing with curl

#### Test Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

#### Test Register
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

#### Test Profile (with token)
```bash
curl -X GET "http://localhost:8000/auth/profile" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Testing with Python Requests

```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/auth/login",
    data={"username": "admin", "password": "admin123"}
)
print(response.json())

# Get token
token = response.json()["access_token"]

# Get profile
response = requests.get(
    "http://localhost:8000/auth/profile",
    headers={"Authorization": f"Bearer {token}"}
)
print(response.json())
```

## Deployment

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t ctp-api .
docker run -p 8000:8000 ctp-api
```

### Cloud Deployment

#### AWS Elastic Beanstalk
```bash
eb init -p python-3.11 ctp-api
eb create ctp-api-env
eb deploy
```

#### Heroku
```bash
heroku create ctp-api
git push heroku main
heroku ps:scale web=1
```

#### DigitalOcean App Platform
1. Connect your repository
2. Select Python runtime
3. Configure build command: `pip install -r requirements.txt`
4. Configure run command: `uvicorn main:app --host 0.0.0.0 --port ${PORT}`

## Project Structure

```
backend/
├── auth/                          # Authentication module
│   ├── __init__.py               # Module exports
│   └── auth.py                   # Auth utilities (JWT, hashing)
│
├── database/                      # Database module
│   ├── __init__.py               # Module exports
│   ├── database.py               # DB configuration & session
│   └── models.py                 # SQLAlchemy models
│
├── routers/                       # API routers
│   ├── __init__.py               # Router exports
│   └── auth_router.py            # Authentication endpoints
│
├── schemas/                       # Pydantic schemas
│   ├── __init__.py               # Schema exports
│   └── schemas.py                # Request/Response models
│
├── scripts/                       # Utility scripts
│   ├── fix_enum/
│   │   └── fix_enum.py           # Fix enum column script
│   ├── init_db/
│   │   ├── init_database.bat     # Windows DB init script
│   │   └── init_db.py            # Database initialization
│   └── start_server/
│       └── start_server.bat      # Windows server start script
│
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore rules
├── main.py                        # FastAPI application
├── requirements.txt               # Python dependencies
├── QUICK_START.md                 # Quick start guide
└── README.md                      # This file
```

### Module Descriptions

#### `auth/`
Contains authentication and authorization logic including password hashing, JWT token creation/validation, and user verification.

#### `database/`
Manages database connections, sessions, and ORM models. Includes the User model with role-based access.

#### `routers/`
API endpoint definitions organized by feature. Currently includes authentication endpoints for login, register, and profile.

#### `schemas/`
Pydantic models for request validation and response serialization. Ensures type safety and automatic API documentation.

#### `scripts/`
Utility scripts for database management and server operations. Organized by purpose in subdirectories.

## Troubleshooting

### Common Issues

#### MySQL Connection Error
```
Error: Can't connect to MySQL server
```
**Solution:** Ensure MySQL is running and credentials in `.env` are correct

#### Port Already in Use
```
Error: [Errno 10048] Address already in use
```
**Solution:** Change the port in `.env` or stop the process using port 8000

#### Import Errors
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution:** Ensure virtual environment is activated and dependencies are installed

#### Database Not Found
```
Error: Unknown database 'ctp_db'
```
**Solution:** Create the database using the initialization script

### Database Migration Issues

If you encounter enum-related errors:

```bash
python scripts/fix_enum/fix_enum.py
```

Or run this SQL manually:
```sql
USE ctp_db;
ALTER TABLE users 
MODIFY COLUMN role 
ENUM('normal', 'admin', 'empresario') 
DEFAULT 'normal' NOT NULL;
```

## API Response Formats

### Success Response
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "string",
    "email": "string",
    "role": "normal|admin|empresario",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### Error Response
```json
{
  "detail": "Error message description"
}
```

## Performance Considerations

### Database Connection Pool
SQLAlchemy connection pool is configured with:
- `pool_pre_ping=True`: Verify connections before use
- `pool_recycle=3600`: Recycle connections after 1 hour

### Optimization Tips
1. Use connection pooling for better performance
2. Enable database query logging only in development
3. Use appropriate indexes on frequently queried columns
4. Implement caching for frequently accessed data
5. Use async endpoints for I/O-bound operations

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use strong database passwords
- [ ] Configure CORS for specific origins in production
- [ ] Enable HTTPS/TLS in production
- [ ] Set appropriate token expiration times
- [ ] Implement rate limiting
- [ ] Use environment variables for sensitive data
- [ ] Regular security updates of dependencies
- [ ] Enable database query logging for monitoring
- [ ] Implement request validation and sanitization

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Update documentation
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review API documentation at `/docs`

## Changelog

### Version 1.0.0 (2024-01-12)
- Initial release
- JWT authentication implementation
- Role-based access control
- User registration and login
- MySQL database integration
- Interactive API documentation
- Modular project structure

---

Built with FastAPI for the Caribbean Enterprises mobile application
