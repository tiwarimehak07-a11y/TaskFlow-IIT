from quick_add import parse_task
from sqlalchemy.orm import Session
import models
from algorithms import insertion_sort, linear_search, binary_search
import schemas
from auth import hash_password, verify_password

# -------------------------
# USER CRUD
# -------------------------

def create_user(db: Session, user: schemas.UserCreate):

    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def login_user(db: Session, email: str, password: str):

    user = db.query(models.User).filter(
        models.User.email == email
    ).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


def get_users(db: Session):
    return db.query(models.User).all()


# -------------------------
# PROJECT CRUD
# -------------------------

def create_project(db: Session, project: schemas.ProjectCreate):

    db_project = models.Project(
        name=project.name,
        owner_id=project.owner_id
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


def get_projects(db: Session):
    return db.query(models.Project).all()


# UPDATE PROJECT
def update_project(
    db: Session,
    project_id: int,
    project: schemas.ProjectCreate
):

    db_project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not db_project:
        return None

    db_project.name = project.name
    db_project.owner_id = project.owner_id

    db.commit()
    db.refresh(db_project)

    return db_project



# DELETE PROJECT
def delete_project(
    db: Session,
    project_id: int
):

    db_project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not db_project:
        return None

    db.delete(db_project)
    db.commit()

    return db_project


# -------------------------
# TASK CRUD
# -------------------------

def create_task(
    db: Session,
    task: schemas.TaskCreate,
    user_id: int
):

    db_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        project_id=task.project_id,
        user_id=user_id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

def get_tasks(
    db: Session,
    sort: str = None,
    status: str = None,
    priority: str = None
):

    query = db.query(models.Task)

    # Status filter
    if status:
        query = query.filter(
            models.Task.status == status
        )

    # Priority filter
    if priority:
        query = query.filter(
            models.Task.priority == priority
        )

    tasks = query.all()

    # Use our own insertion sort
    if sort == "priority":

        records = []

        for task in tasks:

            records.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "priority_rank": {
                    "low": 1,
                    "medium": 2,
                    "high": 3
                }[task.priority],
                "due_date": task.due_date,
                "project_id": task.project_id
            })

        insertion_sort(records, "priority_rank") 
        
        return records

    return tasks


def get_task(db: Session, task_id: int):

    return db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()


def update_task(db: Session, task_id: int, task: schemas.TaskCreate):

    db_task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not db_task:
        return None

    db_task.title = task.title
    db_task.description = task.description
    db_task.status = task.status
    db_task.priority = task.priority
    db_task.due_date = task.due_date
    db_task.project_id = task.project_id

    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(db: Session, task_id: int):

    db_task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not db_task:
        return None

    db.delete(db_task)
    db.commit()

    return db_task

from sqlalchemy import func


def get_task_statistics(db: Session):

    statistics = (
        db.query(
            models.Task.project_id,
            func.count(models.Task.id).label("total_tasks")
        )
        .group_by(models.Task.project_id)
        .all()
    )

    return statistics

def quick_add_task(
    db: Session,
    description: str,
    project_id: int,
    user_id: int
):

    parsed = parse_task(description)

    task = models.Task(
        title=parsed["title"],
        description=description,
        status="pending",
        priority=parsed["priority"],
        due_date=parsed["due_date"],
        project_id=project_id,
        user_id=user_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def search_task(
    db: Session,
    title: str,
    algo: str = "binary"
):

    tasks = db.query(models.Task).all()

    print("TOTAL TASKS:", len(tasks))

    records = []

    for task in tasks:

        print("DB TITLE:", repr(task.title))

        records.append(
            {
                "id": task.id,
                "title": task.title
            }
        )



    if algo == "linear":

        index = linear_search(
            records,
            title,
            "title"
        )

    else:

        insertion_sort(
            records,
            "title"
        )

        print("SORTED RECORDS:", records)
        print("SEARCHING FOR:", title)

        index = binary_search(
            records,
            title,
            "title"
        )

    print("FOUND INDEX:", index)
    
    if index == -1:
        return None

    task_id = records[index]["id"]

    return db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()