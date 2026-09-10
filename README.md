# Personal Details API

An Express and MongoDB API for managing employee personal details.

## Requirements

- Node.js 18 or later
- A MongoDB connection string

## Setup

1. Install dependencies:

   ```bash
   cd backend
   npm install
   ```

2. Create `backend/.env` with your connection details:

   ```env
   MONGO_URI=your_mongodb_connection_string
   PORT=5000
   CLIENT_URL=http://localhost:5173
   NODE_ENV=development
   ```

3. Start the API:

   ```bash
   npm run dev
   ```

The API runs at `http://localhost:5000` by default.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | Health check |
| GET | `/api/employees` | List employees; supports `page` and `limit` query parameters |
| GET | `/api/employees/:id` | Get an employee |
| POST | `/api/employees` | Create an employee |
| PUT | `/api/employees/:id` | Update an employee |
| DELETE | `/api/employees/:id` | Delete an employee |

Employee records require `fullName`, `employeeId`, `email`, and `phone`. Employee IDs follow the format `EMP001`, and email addresses must use the `@snsgroups.com` domain.
