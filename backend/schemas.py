from typing import Optional, Literal

from pydantic import BaseModel, Field, field_validator


# -------------------------
# USER SCHEMAS
# -------------------------

class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = {
        "from_attributes": True
    }


class LoginRequest(BaseModel):
    email: str
    password: str



# -------------------------
# PROJECT SCHEMAS
# -------------------------

class ProjectCreate(BaseModel):
    name: str
    owner_id: int


class ProjectResponse(ProjectCreate):
    id: int

    model_config = {
        "from_attributes": True
    }



# -------------------------
# TASK SCHEMAS
# -------------------------

class TaskCreate(BaseModel):

    title: str

    description: Optional[str] = None

    status: str = "pending"


    priority: Literal["low", "medium", "high"] = Field(
        description="Task priority"
    )

    due_date: Optional[str] = None
    project_id: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):

        if not value.strip():
            raise ValueError("Title cannot be empty")

        return value

class QuickTaskRequest(BaseModel):
     description: str
     project_id: int


class TaskResponse(TaskCreate):

    id: int


    model_config = {
        "from_attributes": True
    }

class QuickTaskResponse(BaseModel):
    message: str
    task: TaskResponse


# -------------------------
# STATISTICS SCHEMA
# -------------------------

class TaskStatistics(BaseModel):

    project_id: int

    total_tasks: int