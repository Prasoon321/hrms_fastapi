# HRMS Lite Backend - FastAPI + MongoDB

## Overview

This is the backend API for HRMS Lite, a lightweight Human Resource Management System built with FastAPI and MongoDB.

## Features

- ✅ Employee Management (CRUD)
- ✅ Attendance Tracking
- ✅ RESTful API
- ✅ MongoDB Integration
- ✅ Input Validation
- ✅ CORS Support
- ✅ Error Handling

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── database.py             # MongoDB connection
│   ├── models/
│   │   ├── employee_model.py   # Employee data model
│   │   └── attendance_model.py # Attendance data model
│   ├── schemas/
│   │   ├── employee_schema.py  # Employee request/response schemas
│   │   └── attendance_schema.py # Attendance request/response schemas
│   ├── routes/
│   │   ├── employee_routes.py  # Employee endpoints
│   │   └── attendance_routes.py # Attendance endpoints
│   ├── services/
│   │   ├── employee_service.py  # Employee business logic
│   │   └── attendance_service.py # Attendance business logic
│   └── utils/
│       └── validators.py       # Validation utilities
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README_BACKEND.md          # This file
```

## Prerequisites

- Python 3.9+
- MongoDB 4.0+ (Local or Cloud)
- pip or poetry

## Installation & Setup

### 1. Install MongoDB Locally

**Windows:**

- Download from: https://www.mongodb.com/try/download/community
- Follow installation wizard
- MongoDB runs on `mongodb://localhost:27017` by default

**Or Use MongoDB Atlas (Cloud):**

- Go to https://www.mongodb.com/cloud/atlas
- Create free cluster
- Get connection string: `mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority`

### 2. Set Up Python Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (Python 3.9+)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your MongoDB connection details
# Default for local MongoDB:
# MONGODB_URL=mongodb://localhost:27017
# DATABASE_NAME=hrms_lite
```

### 5. Run the Backend Server

```bash
# Start the server
python -m uvicorn app.main:app --reload

# Server will start at http://localhost:8000
```

Check health:

```
GET http://localhost:8000/
GET http://localhost:8000/health
```

API Documentation (Swagger UI):

```
http://localhost:8000/docs
```

## API Endpoints

### Employee Management

#### Create Employee

```
POST /employees
Content-Type: application/json

{
  "full_name": "Aarav Sharma",
  "email": "aarav@company.com",
  "department": "IT"
}

Response: 201 Created
{
  "employee_id": "EMP001",
  "full_name": "Aarav Sharma",
  "email": "aarav@company.com",
  "department": "IT",
  "created_at": "2025-02-06T10:00:00"
}
```

#### Get All Employees

```
GET /employees

Response: 200 OK
[
  {
    "employee_id": "EMP001",
    "full_name": "Aarav Sharma",
    "email": "aarav@company.com",
    "department": "IT",
    "created_at": "2025-02-06T10:00:00"
  }
]
```

#### Get Specific Employee

```
GET /employees/{employee_id}
Example: GET /employees/EMP001

Response: 200 OK
{
  "employee_id": "EMP001",
  "full_name": "Aarav Sharma",
  "email": "aarav@company.com",
  "department": "IT",
  "created_at": "2025-02-06T10:00:00"
}
```

#### Delete Employee

```
DELETE /employees/{employee_id}
Example: DELETE /employees/EMP001

Response: 200 OK
{
  "message": "Employee EMP001 deleted successfully"
}
```

### Attendance Management

#### Mark Attendance

```
POST /attendance
Content-Type: application/json

{
  "employee_id": "EMP001",
  "date": "2025-02-06",
  "status": "Present"
}

Valid statuses: Present, Absent, Half Day, Leave

Response: 201 Created
{
  "employee_id": "EMP001",
  "date": "2025-02-06",
  "status": "Present",
  "created_at": "2025-02-06T10:00:00"
}
```

#### Get All Attendance Records

```
GET /attendance

Response: 200 OK
{
  "records": [
    {
      "employee_id": "EMP001",
      "employee_name": "Aarav Sharma",
      "date": "2025-02-06",
      "status": "Present",
      "created_at": "2025-02-06T10:00:00"
    }
  ],
  "total": 1
}
```

#### Get Employee Attendance Records

```
GET /attendance/{employee_id}
Example: GET /attendance/EMP001

Response: 200 OK
[
  {
    "employee_id": "EMP001",
    "date": "2025-02-06",
    "status": "Present",
    "created_at": "2025-02-06T10:00:00"
  }
]
```

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid input data
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource already exists (e.g., duplicate email)
- `500 Internal Server Error`: Server error

### Example Error Responses

Invalid email:

```
POST /employees
Status: 400 Bad Request
{
  "detail": "Invalid email format"
}
```

Employee not found:

```
GET /employees/EMP999
Status: 404 Not Found
{
  "detail": "Employee EMP999 not found"
}
```

Duplicate email:

```
POST /employees
Status: 409 Conflict
{
  "detail": "Email already exists"
}
```

## Validation Rules

### Employee

- `full_name`: Required, 1-100 characters
- `email`: Required, valid email format, unique
- `department`: Required, 1-50 characters

### Attendance

- `employee_id`: Required, must exist
- `date`: Required, format YYYY-MM-DD
- `status`: Required, one of: Present, Absent, Half Day, Leave

## Database Schema

### Employees Collection

```javascript
{
  _id: ObjectId,
  employee_id: "EMP001",        // Unique
  full_name: "Aarav Sharma",
  email: "aarav@company.com",    // Unique
  department: "IT",
  created_at: ISODate("2025-02-06T10:00:00")
}
```

### Attendance Collection

```javascript
{
  _id: ObjectId,
  employee_id: "EMP001",
  date: "2025-02-06",
  status: "Present",
  created_at: ISODate("2025-02-06T10:00:00")
}
```

**Indexes:**

- `employees`: Unique index on `employee_id` and `email`
- `attendance`: Unique index on (`employee_id`, `date`)

## Testing the API

### Using cURL

```bash
# Create employee
curl -X POST http://localhost:8000/employees \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Aarav Sharma","email":"aarav@company.com","department":"IT"}'

# Get all employees
curl http://localhost:8000/employees

# Mark attendance
curl -X POST http://localhost:8000/attendance \
  -H "Content-Type: application/json" \
  -d '{"employee_id":"EMP001","date":"2025-02-06","status":"Present"}'

# Get all attendance
curl http://localhost:8000/attendance
```

### Using Postman

1. Import the API endpoints into Postman
2. Use the examples provided in the API Endpoints section above

### Using Swagger UI

Visit: `http://localhost:8000/docs`

## Frontend Integration

The frontend connects to this API using the following base URL:

```
http://localhost:8000
```

For production, update the API URL in your frontend `.env` file:

```
NEXT_PUBLIC_API_URL=http://your-backend-domain.com
```

## Troubleshooting

### MongoDB Connection Error

```
Error: connect ECONNREFUSED 127.0.0.1:27017
```

**Solution**: Ensure MongoDB is running

```bash
# Windows - MongoDB should be running as service
# macOS - Run: brew services start mongodb-community
# Linux - Run: sudo systemctl start mongod
```

### Port Already in Use

```
Error: Address already in use 0.0.0.0:8000
```

**Solution**: Change the port or kill the process using port 8000

### CORS Error

The API is configured with `allow_origins=["*"]` for development.
In production, update `app/main.py`:

```python
allow_origins=["https://your-frontend-domain.com"],
```

## Deployment

### Docker Deployment

Create a `Dockerfile` in the backend directory:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t hrms-lite-api .
docker run -p 8000:8000 -e MONGODB_URL=... hrms-lite-api
```

## Support & Documentation

- FastAPI Docs: https://fastapi.tiangolo.com/
- MongoDB Docs: https://docs.mongodb.com/
- Uvicorn Docs: https://www.uvicorn.org/

## License

This project is open source and available for educational purposes.
