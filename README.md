## AUTHOR ##
MEHAK

## Installation & Running the Project

```bash
git clone https://github.com/tiwarimehak07-a11y/TaskFlow-IIT.git

cd TaskFlow-IIT

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

Frontend:
Open the `frontend/index.html` file in your browser or serve it using a local web server.

# TaskFlow

A Full-Stack, AI-Assisted Task Management Platform.

## Project Overview

This project is developed as part of the IIT Patna Capstone Project.

More details will be added as the project progresses.

## Tech Stack Section -1 CORE APPLICATIONS:-

Backend:
- FastAPI
- SQLAlchemy ORM
- SQLite Database
- Pydantic
- JWT Authentication
- bcrypt Password Hashing

Frontend:
- HTML
- CSS
- JavaScript
- Fetch API

---

## Database Models

The application contains three main tables:

### User
- id
- name
- email
- password

### Project
- id
- name
- owner_id

### Task
- id
- title
- description
- status
- priority
- due_date
- project_id
- user_id

Relationships:

- One user can create multiple projects.
- One project can contain multiple tasks.
- Tasks are linked with users and projects.

---

## Authentication

Implemented secure authentication using:

- Password hashing using bcrypt
- JWT token generation after login
- Token verification for protected routes

Authentication APIs:
POST /signup
POST /login

## Project APIs

Implemented CRUD operations:

POST /projects
GET /projects
PUT /projects/{project_id}
DELETE /projects/{project_id}

## Task APIs

Implemented CRUD operations:

POST /tasks
GET /tasks
GET /tasks/{task_id}
PUT /tasks/{task_id}
DELETE /tasks/{task_id}

Additional features:

- Filter tasks by status
- Filter tasks by priority
- Task statistics API
- Custom request logging middleware

### Create Task

POST /tasks

Request:

```json
{
  "title": "Complete Backend",
  "description": "Section B testing",
  "status": "pending",
  "priority": "high",
  "due_date": "2026-08-10",
  "project_id": 1
}
```

Response:

```json
{
  "id": 1,
  "title": "Complete Backend",
  "description": "Section B testing",
  "status": "pending",
  "priority": "high",
  "due_date": "2026-08-10",
  "project_id": 1
}
```

API Examples
Authentication
Signup

POST /signup

Request

{
  "name": "Mehak",
  "email": "mehak0706@gmail.com",
  "password": "123456"
}

Response

{
  "id": 1,
  "name": "Mehak",
  "email": "mehak0706@gmail.com"
}
Login

POST /login

Request

username: mehak0706@gmail.com
password: 123456

Response

{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
Project API
Create Project

POST /projects

Request

{
  "name": "TaskFlow",
  "owner_id": 1
}

Response

{
  "id": 1,
  "name": "TaskFlow",
  "owner_id": 1
}
List Projects

GET /projects

Response

[
  {
    "id": 1,
    "name": "TaskFlow",
    "owner_id": 1
  }
]
Task API
Create Task

POST /tasks

Request

{
  "title": "Complete Backend",
  "description": "Section B testing",
  "status": "pending",
  "priority": "high",
  "due_date": "2026-08-10",
  "project_id": 1
}

Response

{
  "id": 1,
  "title": "Complete Backend",
  "description": "Section B testing",
  "status": "pending",
  "priority": "high",
  "due_date": "2026-08-10",
  "project_id": 1
}
List Tasks

GET /tasks

Response

[
  {
    "id": 1,
    "title": "Complete Backend",
    "status": "pending",
    "priority": "high"
  }
]
Get Task by ID

GET /tasks/1

Response

{
  "id": 1,
  "title": "Complete Backend",
  "status": "pending",
  "priority": "high"
}
Update Task

PUT /tasks/1

Request

{
  "title": "Complete Backend Updated",
  "description": "Updated description",
  "status": "completed",
  "priority": "medium",
  "due_date": "2026-08-12",
  "project_id": 1
}

Response

{
  "id": 1,
  "title": "Complete Backend Updated",
  "status": "completed",
  "priority": "medium"
}
Delete Task

DELETE /tasks/1

Response

{
  "message": "Task deleted successfully"
}
Task Statistics

GET /statistics

Response

[
  {
    "project_id": 1,
    "total_tasks": 5
  }
]
Sorted Tasks

GET /tasks?sort=priority

Response

[
  {
    "id": 1,
    "title": "Complete Backend",
    "priority": "high",
    "priority_rank": 3
  }
]
Search Tasks

GET /tasks/search?title=Complete Backend&algo=binary

Response

{
  "id": 1,
  "title": "Complete Backend",
  "priority": "high"
}
AI Quick Add

POST /tasks/quick-add

Request

{
  "description": "Complete backend urgent tomorrow",
  "project_id": 1
}

Response

{
  "message": "Quick task created successfully",
  "task": {
    "title": "Complete backend",
    "priority": "high",
    "due_date": "tomorrow"
  }
}
Also add these two sections at the end of your Section 3.
Prompting Technique Rationale

## Prompting Technique Rationale

The AI Quick Add feature uses a deterministic rule-based parser instead of an external Large Language Model. The parser analyzes keywords in the user's task description to determine task priority, due date, and task title. This approach requires no API keys, no internet connection, produces deterministic outputs, and fully satisfies the project requirement for an offline mock parser.
Worked Examples
## Worked Examples

| User Input | Generated Title | Priority | Due Date |
|------------|-----------------|----------|----------|
| Complete backend urgent tomorrow | Complete backend | High | tomorrow |
| Finish report asap | Finish report | High | None |
| Buy groceries today | Buy groceries | Medium | today |
| Learn Docker whenever | Learn Docker | Low | None |
| Submit assignment | Submit assignment | Medium | None |

## Frontend Features

Frontend provides:

- Add new task
- View all tasks
- Edit task
- Delete task
- Project selection
- Backend API integration using Fetch API


# Section 2 — Integrated Algorithms Engine

## Overview

TaskFlow uses custom hand-written sorting and searching algorithms as the engine behind task sorting and searching features. These algorithms operate on real task data fetched from the same SQLAlchemy database used by the application.

Python built-in functions like `sorted()` and `list.sort()` are not used.

## Implemented Algorithms

### 1. Insertion Sort

Function:
insertion_sort(records, key)

The algorithm sorts records in-place by comparing elements with previous elements and shifting them to their correct position.

Used in:
GET /tasks?sort=priority

Priority mapping:

low = 1
medium = 2
high = 3

### 2. Binary Search

Function:

binary_search(sorted_records, target_value, key)
Binary search works on a list already sorted using insertion sort and returns the index of the matching record.

Used in:
GET /tasks/search?title=<title>&algo=binary

### 3. Linear Search

Function:

linear_search(records, target_value, key)
Linear search checks each record sequentially and is used as a baseline comparison.

Used in:
GET /tasks/search?title=<title>&algo=linear

# API Integration

## Task Sorting

Endpoint:
GET /tasks?sort=priority

Flow:
1. Tasks are fetched from the database.
2. Task priority is converted into comparable ranking values.
3. Custom insertion sort is applied.
4. Sorted tasks are returned as JSON.

## Task Searching

Endpoint:
GET /tasks/search?title=<title>&algo=binary|linear

Flow:
1. Task records are fetched from the database.
2. An in-memory index containing task IDs and titles is created.
3. Binary search or linear search is applied.
4. Matching task is returned.

# Algorithm Complexity Analysis

| Algorithm | Best Case | Worst Case |
|----------|-----------|------------|
| Insertion Sort | O(n) | O(n²) |
| Binary Search | O(1) | O(log n) |
| Linear Search | O(1) | O(n) |

# Benchmark Results

The algorithms were tested using comparison-counting wrapper functions:

- insertion_sort_count()
- binary_search_count()
- linear_search_count()

Testing was performed on task-like datasets of sizes:

- 10 records
- 500 records
- 3000 records

Raw benchmark numbers are stored in:
benchmark_results.txt

# Benchmark Analysis

The benchmark results show that insertion sort requires more comparisons as the number of tasks increases.

For 3000 records, insertion sort required:


1,820,009 comparisons

while binary search required only:

11 comparisons
This shows that although sorting has an initial cost, it allows faster repeated searching. Since TaskFlow users are expected to view and organize tasks frequently while adding or renaming tasks less often, sorting the task list first provides better performance for repeated operations.

# Automated Algorithm Checks

A validation script was created:
check_algorithms.py

It verifies:

- Empty list sorting
- Single element sorting
- Binary search first, middle and last positions
- Binary search not found case
- Sorting comparison count
- Binary search comparison count
- Linear search comparison count

Run command:
python check_algorithms.py
All test cases pass successfully.

# Section 3 — AI Quick Add

## Overview

TaskFlow includes an AI-assisted Quick Add feature that converts free-text task descriptions into structured task records.

## Endpoint

POST /tasks/quick-add

## Request Body

```json
{
  "description": "Complete backend urgent tomorrow",
  "project_id": 1
}
```

## Parsing Rules

The parser extracts:

- Task title
- Priority
- Due date

Priority detection:

- "urgent", "asap" → high
- "whenever", "low priority" → low
- otherwise → medium

Due date detection:

- "today"
- "tomorrow"

The generated task is automatically saved into the database and linked with the authenticated user.

## API Documentation

Swagger UI:

http://127.0.0.1:8000/docs

## Future Improvements

- Notifications
- Email reminders
- AI task categorization

Last updated for final submission.