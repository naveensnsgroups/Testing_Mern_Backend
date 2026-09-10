# Personal Details App - FastAPI Backend

Migrated from Express.js to Python FastAPI, Motor (Async MongoDB driver), and Pydantic v2.

## Features

- **FastAPI**: Modern, high-performance async web framework.
- **Motor / PyMongo**: Asynchronous MongoDB operations connected to MongoDB Atlas.
- **Pydantic v2**: Strict request validation enforcing exact rules:
  - `fullName`: Letters and spaces only, max 100 chars.
  - `employeeId`: Must start with `EMP` followed by numbers (e.g. `EMP001`), max 20 chars.
  - `email`: Lowercase, ending with `@snsgroups.com`, max 150 chars.
  - `phone`: Exactly 10 digits.
  - Enums for `gender` (`Male`, `Female`, `Other`) and `department` (`IT`, `HR`, `Finance`, `Marketing`, `Operations`, `Sales`, `Admin`, `Other`).
- **Exact API Response Structure**: Preserves identical JSON success, error, pagination, and status codes (`201 Created`, `400 Bad Request`, `404 Not Found`, `409 Conflict`, `500 Internal Server Error`).

## Setup & Running

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and configure your `MONGO_URI`:
   ```bash
   cp .env.example .env
   ```

3. Run the development server with Uvicorn:
   ```bash
   uvicorn app.main:app --reload --port 5000
   ```

4. Access interactive API docs at:
   - Swagger UI: `http://localhost:5000/docs`
   - ReDoc: `http://localhost:5000/redoc`
