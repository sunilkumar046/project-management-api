from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MemberAdd(BaseModel):
    user_id: int
class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    role: Optional[str] = "Member"


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str

    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    name: str
    description: str


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    created_by: int

    class Config:
        from_attributes = True
class TaskCreate(BaseModel):
    title: str
    description: str
    priority: str
    due_date: datetime
    assigned_to: int
    project_id: int

class TaskUpdate(BaseModel):
    title: str
    description: str
    status: str
    priority: str
    due_date: datetime

class TaskStatusUpdate(BaseModel):
    status: str


class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    is_read: bool

class ActivityResponse(BaseModel):
    id: int
    action: str
    entity_type: str
    description: str
    created_at: datetime

class AuditLogResponse(BaseModel):
    id: int
    entity_type: str
    field_name: str
    old_value: str | None
    new_value: str | None