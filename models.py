from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base
from sqlalchemy import Boolean


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="Member")

    projects = relationship("Project", back_populates="creator")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

    created_by = Column(
        Integer,
        ForeignKey("users.id")
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    creator = relationship(
        "User",
        back_populates="projects"
    )


class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id")
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)

    status = Column(
        String,
        default="Pending"
    )

    priority = Column(String)

    due_date = Column(DateTime)

    assigned_to = Column(
        Integer,
        ForeignKey("users.id")
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id")
    )


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    action = Column(String)

    entity_type = Column(String)

    entity_id = Column(Integer)

    description = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index = True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    title = Column(String)

    message = Column(String)

    is_read = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index = True)

    entity_type = Column(String)

    entity_id = Column(Integer)

    field_name = Column(String)

    old_value = Column(String)

    new_value = Column(String)

    changed_by = Column(Integer)

    changed_at = Column(
        DateTime,
        default=datetime.utcnow
    )