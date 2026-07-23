from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from models import Project
from dependencies import role_required
from sqlalchemy.orm import Session
from dependencies import get_current_user
import models
import schemas
from fastapi.security import OAuth2PasswordRequestForm
from database import engine
from database import get_db
from models import (
    User,
    Project,
    ProjectMember,
    Task,
    Notification,
    ActivityLog,
    AuditLog
)

from security import hash_password
from security import verify_password
from security import create_access_token

app = FastAPI()

models.Base.metadata.create_all(
    bind=engine
)

@app.get("/auth/me")
def me(current_user=Depends(get_current_user)):
    return current_user

@app.get("/")
def home():
    return {
        "message": "Project Management API"
    }


@app.post("/auth/signup")
def signup(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(
            user.password
        ),
        role=user.role
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User created"
    }




@app.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )

    if not verify_password(
        form_data.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    token = create_access_token(
        {"sub": db_user.email}
    )

    # Activity Log
    activity = ActivityLog(
        user_id=db_user.id,
        action="LOGIN",
        entity_type="USER",
        entity_id=db_user.id,
        description="User Logged In"
    )

    db.add(activity)
    db.commit()

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.post("/projects")
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(["Admin", "Manager"])
    )
):

    new_project = Project(
        name=project.name,
        description=project.description,
        created_by=current_user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    activity = ActivityLog(
        user_id=current_user.id,
        action="PROJECT_CREATED",
        entity_type="PROJECT",
        entity_id=new_project.id,
        description=f"Project '{new_project.name}' created"
    )

    db.add(activity)
    db.commit()

    return {
        "message": "Project Created"
    }

@app.post("/projects/{project_id}/members")
def add_member(
    project_id: int,
    member: schemas.MemberAdd,
    db: Session = Depends(get_db)
):

    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    user = db.query(User).filter(
        User.id == member.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    project_member = ProjectMember(
        project_id=project_id,
        user_id=member.user_id
    )

    db.add(project_member)
    db.commit()

    return {
        "message": "Member added successfully"
    }

@app.post("/tasks")
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(["Admin", "Manager"])
    )
):

    project = db.query(Project).filter(
        Project.id == task.project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    user = db.query(User).filter(
        User.id == task.assigned_to
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        due_date=task.due_date,
        assigned_to=task.assigned_to,
        project_id=task.project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # Activity Log
    activity = ActivityLog(
        user_id=current_user.id,
        action="TASK_CREATED",
        entity_type="TASK",
        entity_id=new_task.id,
        description=f"Task '{new_task.title}' created"
    )

    db.add(activity)

    # Notification
    notification = Notification(
        user_id=user.id,
        title="New Task Assigned",
        message=f"You have been assigned task '{new_task.title}'"
    )

    db.add(notification)

    db.commit()

    return {
        "message": "Task Created"
    }

@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    updated_task: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.title = updated_task.title
    task.description = updated_task.description
    task.status = updated_task.status
    task.priority = updated_task.priority
    task.due_date = updated_task.due_date

    db.commit()

    return {
        "message": "Task Updated"
    }


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task Deleted"
    }
@app.put("/projects/{project_id}")
def update_project(
    project_id: int,
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(["Admin", "Manager"])
    )
):
    db_project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    db_project.name = project.name
    db_project.description = project.description

    db.commit()

    return {
        "message": "Project Updated"
    }

@app.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(["Admin"])
    )
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    db.delete(project)
    db.commit()

    return {
        "message": "Project Deleted"
    }

@app.put("/tasks/{task_id}/status")
def update_task_status(
    task_id: int,
    task_data: schemas.TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(["Member"])
    )
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    old_status = task.status

    task.status = task_data.status

    db.commit()

    audit = AuditLog(
        entity_type="TASK",
        entity_id=task.id,
        field_name="status",
        old_value=old_status,
        new_value=task_data.status,
        changed_by=current_user.id
    )

    db.add(audit)
    db.commit()

    activity = ActivityLog(
        user_id=current_user.id,
        action="TASK_STATUS_CHANGED",
        entity_type="TASK",
        entity_id=task.id,
        description=f"Status changed from {old_status} to {task_data.status}"
    )

    db.add(activity)
    db.commit()

    return {
        "message": "Task Status Updated"
    }

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.assigned_to != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not your task"
        )

    task.status = task_data.status

    db.commit()

    return {
        "message": "Status Updated"
    }

@app.get("/projects/{project_id}/members")
def get_project_members(
    project_id: int,
    db: Session = Depends(get_db)
):
    members = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id
    ).all()

    return members

@app.get("/notifications")
def get_notifications(db: Session = Depends(get_db)):
    return db.query(Notification).all()


@app.put("/notifications/{id}/read")
def mark_read(id: int, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(
        Notification.id == id
    ).first()

    notification.is_read = True

    db.commit()

    return {"message": "Notification Read"}


@app.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    return db.query(ActivityLog).all()


@app.get("/activities/user/{user_id}")
def get_user_activities(
    user_id: int,
    db: Session = Depends(get_db)
):
    return db.query(ActivityLog).filter(
        ActivityLog.user_id == user_id
    ).all()


@app.get("/audit-logs")
def get_audit_logs(
    db: Session = Depends(get_db)
):
    return db.query(AuditLog).all()



@app.get("/notifications/unread")
def get_unread_notifications(
    db: Session = Depends(get_db)
):
    return db.query(Notification).filter(
        Notification.is_read == False
    ).all()



@app.put("/notifications/read-all")
def read_all_notifications(
    db: Session = Depends(get_db)
):

    notifications = db.query(
        Notification
    ).all()

    for notification in notifications:
        notification.is_read = True

    db.commit()

    return {
        "message": "All Notifications Read"
    }




@app.delete("/notifications/{id}")
def delete_notification(
    id: int,
    db: Session = Depends(get_db)
):

    notification = db.query(
        Notification
    ).filter(
        Notification.id == id
    ).first()

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    db.delete(notification)
    db.commit()

    return {
        "message": "Notification Deleted"
    }