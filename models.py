from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


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

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

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