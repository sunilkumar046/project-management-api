# Project Management API with RBAC

## Overview

This is a Project Management API built using FastAPI.

The application allows users to:

- Register and Login
- Create and Manage Projects
- Add Members to Projects
- Create and Assign Tasks
- Update Task Status
- Manage Access using User Roles

---

## Technologies Used

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- JWT Authentication
- Passlib (bcrypt)

---

## User Roles

### Admin
- Create Projects
- Update Projects
- Delete Projects
- Assign Tasks
- View All Projects and Tasks

### Manager
- Create Projects
- Assign Tasks
- Manage Project Members
- Update Projects

### Member
- View Assigned Tasks
- Update Task Status
- View Assigned Projects

---

## Database Tables

### Users
- id
- full_name
- email
- password
- role

### Projects
- id
- name
- description
- created_by
- created_at

### Project Members
- id
- project_id
- user_id

### Tasks
- id
- title
- description
- status
- priority
- due_date
- assigned_to
- project_id

---

## API Endpoints

### Authentication
- POST /auth/signup
- POST /auth/login
- GET /auth/me

### Projects
- POST /projects
- GET /projects
- GET /projects/{id}
- PUT /projects/{id}
- DELETE /projects/{id}

### Project Members
- POST /projects/{id}/members
- GET /projects/{id}/members

### Tasks
- POST /tasks
- GET /tasks
- GET /tasks/{id}
- PUT /tasks/{id}
- DELETE /tasks/{id}
- PUT /tasks/{id}/status

---

## Run Project

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Server

```bash
uvicorn main:app --reload
```

### Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

### Author

Sunil Kumar