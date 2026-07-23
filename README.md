# Project Management API with Notification & Activity Tracking

## Overview

This project is a backend application developed using FastAPI that allows users to manage projects and tasks with Role-Based Access Control (RBAC). The application also includes JWT Authentication, Activity Logging, Notifications, and Audit Tracking.

---

## Technologies Used

- Python
- FastAPI
- SQLAlchemy ORM
- SQLite
- Pydantic
- JWT Authentication
- Passlib (bcrypt)

---

## Features

### Authentication

- User Registration
- User Login
- Password Hashing
- JWT Token Authentication
- Protected Routes

### Role-Based Access Control (RBAC)

#### Admin
- Create Projects
- Update Projects
- Delete Projects
- Manage Users
- View All Projects and Tasks

#### Manager
- Create Projects
- Assign Tasks
- Update Projects
- View Project Information

#### Member
- View Assigned Tasks
- Update Task Status

---

## Project Management

Implemented APIs for:

- Create Project
- View Projects
- View Single Project
- Update Project
- Delete Project

Project Fields:

- id
- name
- description
- created_by
- created_at

---

## Project Membership

Implemented APIs for:

- Add Member to Project
- View Project Members

Relationship:

- One Project can have multiple members
- One User can belong to multiple projects

---

## Task Management

Implemented APIs for:

- Create Task
- View Tasks
- View Single Task
- Update Task
- Delete Task
- Update Task Status

Task Fields:

- id
- title
- description
- status
- priority
- due_date
- assigned_to
- project_id

---

## Activity Logging System

The application automatically tracks important user activities.

Activities Tracked:

- User Login
- Project Creation
- Task Creation
- Task Status Change

Activity Log Fields:

- id
- user_id
- action
- entity_type
- entity_id
- description
- created_at

APIs:

- GET /activities
- GET /activities/user/{id}

---

## Notification System

Notifications are automatically generated when important events occur.

Implemented:

- Task Assignment Notification

Notification Features:

- View Notifications
- View Unread Notifications
- Mark Notification as Read
- Mark All Notifications as Read
- Delete Notification

Notification Fields:

- id
- user_id
- title
- message
- is_read
- created_at

APIs:

- GET /notifications
- GET /notifications/unread
- PUT /notifications/{id}/read
- PUT /notifications/read-all
- DELETE /notifications/{id}

---

## Audit Log System

Maintains a history of important changes in the application.

Implemented:

- Task Status Change Tracking

Example:

Pending → In Progress → Completed

Audit Log Fields:

- id
- entity_type
- entity_id
- field_name
- old_value
- new_value
- changed_by
- changed_at

APIs:

- GET /audit-logs

---

## Database Tables

- users
- projects
- project_members
- tasks
- activity_logs
- notifications
- audit_logs

---

## API Documentation

Swagger UI:

http://127.0.0.1:8000/docs

---

## How to Run

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
uvicorn main:app --reload
```

### Open Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

---

## Deliverables

- Source Code
- Updated GitHub Repository
- README Documentation
- Database Schema Diagram
- Swagger Screenshots
- Postman Collection

---

## Conclusion

This project demonstrates FastAPI backend development with Authentication, Authorization, Project Management, Task Management, Activity Tracking, Notifications, and Audit Logging using clean API design and database relationships.