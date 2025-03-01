# Labor Management System

A full-stack application for managing associates, labor assignments, and temporary permissions. Built with Flask (Python) backend and React (Material-UI) frontend.

![image](https://github.com/user-attachments/assets/b557ab4f-6a2d-4c3d-b32b-bae6d8b20b84)


## Features

### Backend (Flask)
- JWT Authentication with role-based access (Admin/Manager)
- Associate CRUD operations
- Labor assignment algorithm with permissions matching
- Temporary change requests workflow
- Case-insensitive path matching for labor assignments
- RESTful API endpoints

### Frontend (React)
- Role-based navigation (Admin/Manager)
- Associate management interface
- Labor assignment form with path selection
- Approval workflow interface
- User management (Admin only)
- Responsive Material-UI components
- Persistent login session

## Tech Stack

**Backend**
- Python 3.9+
- Flask
- Flask-JWT-Extended
- Flask-CORS
- MongoDB
- pymongo

**Frontend**
- React 18+
- React Router 6
- Material-UI (MUI)
- Axios
- React Error Boundary

## Installation

### Prerequisites
- MongoDB instance
- Node.js 16+
- Python 3.9+

### Backend Setup
1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac)
   venv\Scripts\activate  # Windows

### Backend Setup
1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac)
   venv\Scripts\activate  # Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` file:
   ```env
   FLASK_ENV=development
   JWT_SECRET_KEY=your-secret-key
   MONGO_URI=mongodb://localhost:27017/labor_management
   ```
4. Run Flask application:
   ```bash
   python main.py
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start development server:
   ```bash
   npm start
   ```

## API Documentation

### Authentication
| Endpoint       | Method | Description          |
|----------------|--------|----------------------|
| `/api/login`   | POST   | User authentication  |

### Associates
| Endpoint              | Method | Description                     |
|-----------------------|--------|---------------------------------|
| `/associates`         | GET    | Get all associates              |
| `/associates`         | POST   | Create new associate            |
| `/associates/<login>` | GET    | Get single associate            |
| `/associates/<login>` | PUT    | Update associate                |
| `/associates/<login>` | DELETE | Delete associate                |
| `/assign-labor`       | POST   | Assign labor to associates      |

### Temporary Changes
| Endpoint                       | Method | Description              |
|--------------------------------|--------|--------------------------|
| `/temp-changes`                | POST   | Create temp change       |
| `/temp-changes/pending`        | GET    | Get pending changes      |
| `/temp-changes/<change_id>/approve` | POST | Approve change |
| `/temp-changes/<change_id>/reject`  | POST | Reject change  |

## Usage

### Sample Requests

**Login**
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**Create Associate**
```bash
curl -X POST http://localhost:5000/associates \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"login_id":"john_doe","name":"John Doe","permissions":["pick","pack"]}'
```

**Assign Labor**
```bash
curl -X POST http://localhost:5000/assign-labor \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "logins": ["user1", "user2", "user3"],
    "requirements": {"pick": 2, "ttb": 1}
  }'
```

## Frontend Components

### Key Features
- **Labor Assignment Form**
  - Multi-line login input
  - Path selection dropdown
  - Quantity input with validation
  - Visual requirements list
  - Case-insensitive matching

- **Role-Based Navigation**
  - Admins: Approvals, User Management
  - Managers: Labor Requests, Assignments
  - Responsive mobile menu

## Configuration

### Environment Variables
| Variable        | Description                | Example                     |
|-----------------|----------------------------|-----------------------------|
| `JWT_SECRET_KEY`| JWT encryption secret      | `supersecretkey123`         |
| `MONGO_URI`     | MongoDB connection string  | `mongodb://localhost:27017` |

### Database Collections
- `associates`: Stores associate records
- `temp_changes`: Temporary permission requests
- `users`: User credentials (admin/manager)

## License

MIT License

```

This README includes:
1. System overview and features
2. Technology stack
3. Installation instructions
4. API documentation
5. Usage examples
6. Configuration details
7. License information

You can customize it further by:
- Adding screenshots
- Including contribution guidelines
- Adding testing instructions
- Expanding the API documentation
- Adding deployment instructions
