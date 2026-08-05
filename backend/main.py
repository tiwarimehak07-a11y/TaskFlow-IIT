from fastapi import FastAPI, Depends, HTTPException, status
import time
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

import models
import crud
import schemas

from database import engine, Base, get_db
from security import create_access_token, verify_token

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskFlow API",
    version="1.0.0"
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


# -------------------------
# CURRENT USER
# -------------------------

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    email = payload.get("sub")

    user = db.query(models.User).filter(
        models.User.email == email
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@app.middleware("http")
async def log_requests(request, call_next):

    start_time = time.time()

    response = await call_next(request)

    end_time = time.time()

    process_time = (end_time - start_time) * 1000

    print(
        f"{request.method} {request.url.path} - {process_time:.2f} ms"
    )

    return response


# -------------------------
# CORS Configuration
# -------------------------

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE"
    ],
    allow_headers=["*"],
)



# -------------------------
# HOME
# -------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to TaskFlow API"
    }



# -------------------------
# USERS API
# -------------------------

@app.post(
    "/users",
    response_model=schemas.UserResponse,
    status_code=201
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    return crud.create_user(db, user)



@app.get(
    "/users",
    response_model=list[schemas.UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):

    return crud.get_users(db)



# -------------------------
# AUTH API
# -------------------------

@app.post(
    "/signup",
    response_model=schemas.UserResponse,
    status_code=201
)
def signup(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    return crud.create_user(db, user)



@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = crud.login_user(
        db,
        form_data.username,
        form_data.password
    )


    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    access_token = create_access_token(
        {
            "sub": db_user.email
        }
    )


    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# -------------------------
# PROJECTS API
# -------------------------

@app.post(
    "/projects",
    response_model=schemas.ProjectResponse,
    status_code=201
)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db)
):

    return crud.create_project(
        db,
        project
    )



@app.get(
    "/projects",
    response_model=list[schemas.ProjectResponse]
)
def get_projects(
    db: Session = Depends(get_db)
):

    return crud.get_projects(db)

@app.put(
    "/projects/{project_id}",
    response_model=schemas.ProjectResponse
)
def update_project(
    project_id: int,
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db)
):

    return crud.update_project(
        db,
        project_id,
        project
    )



@app.delete(
    "/projects/{project_id}"
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):

    return crud.delete_project(
        db,
        project_id
    )

# -------------------------
# TASKS API
# -------------------------

@app.post(
    "/tasks",
    response_model=schemas.TaskResponse,
    status_code=201
)
@app.post(
    "/tasks",
    response_model=schemas.TaskResponse,
    status_code=201
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return crud.create_task(
        db,
        task,
        current_user.id
    )


@app.get("/tasks")
def get_tasks(
    sort: str = None,
    status: str = None,
    priority: str = None,
    db: Session = Depends(get_db)
):

    return crud.get_tasks(
        db,
        sort,
        status,
        priority
    )

@app.get("/tasks/search")
def search_task(
    title: str,
    algo: str = "binary",
    db: Session = Depends(get_db)
):

    task = crud.search_task(
        db,
        title,
        algo
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

@app.post(
    "/tasks/quick-add",
    response_model=schemas.QuickTaskResponse
)
def quick_add(
    request: schemas.QuickTaskRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    task = crud.quick_add_task(
        db=db,
        description=request.description,
        project_id=request.project_id,
        user_id=current_user.id
    )

    return {
        "message": "Quick task created successfully",
        "task": task
    }


@app.get(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse
)
def get_single_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    return crud.get_task(
        db,
        task_id
    )



@app.put(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse
)
def update_task(
    task_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db)
):

    return crud.update_task(
        db,
        task_id,
        task
    )



@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    crud.delete_task(
        db,
        task_id
    )


    return {
        "message": "Task deleted successfully"
    }


#Statistics API#

@app.get(
    "/statistics",
    response_model=list[schemas.TaskStatistics]
)
def task_statistics(
    db: Session = Depends(get_db)
):

    return crud.get_task_statistics(db)