# 05 — CRUD Operations in FastAPI

## 1. What Is CRUD?

### Simple definition
CRUD represents the four basic operations we perform on data: create it, read it, update it, and delete it.

**Think of a task manager:** You create a task, view your tasks, edit a task, or delete a task.

### Technical definition
CRUD stands for Create, Read, Update, and Delete. These operations are commonly implemented in web APIs using HTTP methods such as POST, GET, PUT, and DELETE.

| Operation | HTTP method | Example endpoint |
|---|---|---|
| Create | `POST` | `/tasks` |
| Read all | `GET` | `/tasks` |
| Read one | `GET` | `/tasks/{task_id}` |
| Update | `PUT` | `/tasks/{task_id}` |
| Delete | `DELETE` | `/tasks/{task_id}` |

---

## 2. What Is an Endpoint?

### Simple definition
An endpoint is a specific API route that a client can request to perform an operation.

### Technical definition
An endpoint is a combination of an HTTP method and a URL path handled by an application.

For example:

```python
@app.get("/tasks")
def get_tasks():
    return temp_database
```

Here, `GET /tasks` is the endpoint. FastAPI calls `get_tasks()` when a matching request arrives.

---

## 3. What Is In-Memory Storage?

In our project, we started with:

```python
temp_database = []
next_task_id = 1
```

### Simple definition
In-memory storage means keeping data in the application's working memory instead of saving it to a permanent database.

### Technical definition
In-memory storage holds data in process memory, such as a Python list or dictionary, while the application is running.

- `temp_database` stores the task dictionaries.
- `next_task_id` tracks the next ID to assign.

For example:

```python
temp_database = [
    {
        "id": 1,
        "title": "Learn Python",
        "description": "Practice loops",
        "completed": False
    }
]
```

**Important:** This is only temporary storage. If the application process restarts, the list resets. Later, we'll replace it with PostgreSQL.

---

## 4. CREATE — POST

### Simple definition
POST is commonly used to create a new resource.

### Technical definition
The HTTP POST method asks the server to process the request body according to the target resource's semantics. In our API, we use it to create a task.

Our endpoint:

```python
@app.post("/tasks")
def create_task(task: Task):
    global next_task_id

    new_task = {
        "id": next_task_id,
        **task.model_dump()
    }

    temp_database.append(new_task)
    next_task_id += 1

    return new_task
```

### How it works

1. FastAPI receives the request body and validates it using the `Task` model.
2. The validated model is available as `task`.
3. `task.model_dump()` converts the model to a Python dictionary.
4. The dictionary is combined with the server-generated ID.
5. `temp_database.append(new_task)` adds the new task to the list.
6. `next_task_id += 1` increments the counter for the next task.
7. `return new_task` sends the created task back to the client.

### What does `global next_task_id` mean?

It tells Python that assignments to `next_task_id` inside this function should update the variable defined at module level, rather than create a local variable with the same name.

### What does `append()` do?

`append()` adds one item to the end of a list.

```python
temp_database.append(new_task)
```

If the list contained two tasks, appending another task would make it contain three.

### Example request body

```json
{
  "title": "Learn Python",
  "description": "Practice loops",
  "completed": false
}
```

Example response:

```json
{
  "id": 1,
  "title": "Learn Python",
  "description": "Practice loops",
  "completed": false
}
```

The server generates the ID, so the client doesn't need to supply it.

---

## 5. READ ALL — GET

### Simple definition
GET is used to retrieve data. In our API, `GET /tasks` returns all stored tasks.

### Technical definition
The HTTP GET method requests a representation of a resource without asking the server to modify that resource.

Our endpoint:

```python
@app.get("/tasks")
def get_tasks():
    return temp_database
```

### How it works

- FastAPI calls `get_tasks()` when a client requests `GET /tasks`.
- `return temp_database` returns the entire list.
- FastAPI serializes the list and its dictionaries into a JSON response.

**Why don't we need a loop?**

Because we're returning the entire list, not searching for or modifying an individual item.

If the list is empty, the response is:

```json
[]
```

---

## 6. READ ONE — GET by ID

### Simple definition
This endpoint retrieves one specific task using its ID.

### Technical definition
The route contains a path parameter that identifies the requested task. The endpoint searches the stored collection for a matching record.

Our endpoint:

```python
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in temp_database:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
```

### Understand the loop

```python
for task in temp_database:
```

This takes each item from `temp_database`, one at a time, and assigns it to `task`.

Although `temp_database` is a list, each `task` is a dictionary.

For example:

```python
task = {
    "id": 2,
    "title": "Learn FastAPI",
    "completed": False
}
```

Here:

- `task["id"]` returns `2`.
- `task["title"]` returns `"Learn FastAPI"`.

### Understand the condition

```python
if task["id"] == task_id:
```

- `task["id"]` is the ID stored in the current task dictionary.
- `task_id` is the ID supplied in the URL.

If the client requests `/tasks/2`, the condition checks whether the current task's ID equals `2`.

### Why return the task?

```python
return task
```

Once the matching task is found, the function returns it and stops. The client receives only that task.

### What is HTTP 404?

**Simple definition:** The requested resource could not be found.

**Technical definition:** `404 Not Found` is an HTTP status code indicating that the server could not find a current representation of the requested resource.

If the loop finishes without finding the ID, the function raises the exception.

---

## 7. UPDATE — PUT

### Simple definition
PUT is commonly used to update an existing resource. In our implementation, it replaces the task's editable fields with the supplied values.

### Technical definition
The HTTP PUT method requests that the target resource be created or replaced with the state represented by the request. Our endpoint uses PUT to replace an existing task's fields; it does not create a missing task.

Our endpoint:

```python
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(temp_database):
        if task["id"] == task_id:
            updated_task_data = {
                "id": task_id,
                **updated_task.model_dump()
            }

            temp_database[index] = updated_task_data
            return updated_task_data

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
```

### What does `updated_task` contain?

The parameter `updated_task: Task` receives the validated request body.

For example, the client sends:

```json
{
  "title": "Learn FastAPI",
  "description": "CRUD completed",
  "completed": true
}
```

FastAPI validates it against `Task`, then makes the resulting Pydantic model available through `updated_task`.

### What does `enumerate()` do?

**Simple definition:** It lets us loop through a list while getting both the position of each item and the item itself.

**Technical definition:** Python's `enumerate()` produces pairs containing an index and the corresponding item from an iterable.

For example:

```python
tasks = ["Python", "FastAPI", "SQL"]

for index, task in enumerate(tasks):
    print(index, task)
```

Output:

```text
0 Python
1 FastAPI
2 SQL
```

In our endpoint:

- `index` is the position in the list.
- `task` is the dictionary at that position.

Remember: **a task's ID is not necessarily the same as its list index.**

### What does `updated_task.model_dump()` do?

It converts the incoming Pydantic model into a Python dictionary.

For example:

```python
updated_task.model_dump()
```

produces:

```python
{
    "title": "Learn FastAPI",
    "description": "CRUD completed",
    "completed": True
}
```

### Why do we use `**updated_task.model_dump()`?

The `**` unpacks those dictionary fields into a new dictionary.

```python
updated_task_data = {
    "id": task_id,
    **updated_task.model_dump()
}
```

The result is:

```python
{
    "id": 2,
    "title": "Learn FastAPI",
    "description": "CRUD completed",
    "completed": True
}
```

The ID comes from the URL parameter, while the editable fields come from the request body.

### How does the replacement happen?

```python
temp_database[index] = updated_task_data
```

This replaces the existing dictionary at that list position.

It does **not** add a new task, so the number of tasks stays the same.

### Why return the updated task?

```python
return updated_task_data
```

This lets the client see the new values in the response.

### Why return 404 if no task matches?

If the loop finishes without finding the requested ID, there is no existing task to update. Our implementation raises `HTTPException` with status code `404`.

**Important:** This PUT endpoint expects the full set of editable fields. For a partial update, we would typically design a PATCH endpoint.

---

## 8. DELETE — DELETE

### Simple definition
DELETE removes a resource. In our API, it removes one task identified by its ID.

### Technical definition
The HTTP DELETE method requests the removal of the association between the target resource and its current functionality. Our endpoint removes the matching task from the in-memory list.

Our endpoint:

```python
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in temp_database:
        if task["id"] == task_id:
            temp_database.remove(task)
            return {
                "message": "Task deleted",
                "id": task_id
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
```

### How it works

1. The client supplies a task ID in the URL.
2. The loop searches for the matching task.
3. `temp_database.remove(task)` removes that dictionary from the list.
4. The endpoint returns a confirmation.
5. If no task matches, it raises a `404` exception.

### What does `remove()` do?

`remove()` removes the first matching item from a list.

```python
numbers = [10, 20, 30]
numbers.remove(20)
```

The list becomes:

```python
[10, 30]
```

In our API, we pass the matching task dictionary to `remove()`.

---

## 9. What Is `HTTPException`?

### Simple definition
`HTTPException` lets an endpoint stop normal processing and return an HTTP error response.

### Technical definition
FastAPI's `HTTPException` is an exception class used to produce an HTTP response with a specified status code and detail.

We import it using:

```python
from fastapi import HTTPException
```

Example:

```python
raise HTTPException(
    status_code=404,
    detail="Task not found"
)
```

This produces a response like:

```json
{
  "detail": "Task not found"
}
```

with HTTP status `404`.

The `raise` keyword raises the exception, so the function doesn't continue as if the request had succeeded.

---

## 10. How to Test CRUD in Swagger

Swagger UI lets you send API requests and inspect their responses without writing a separate client.

Open:

```text
http://127.0.0.1:8000/docs
```

### Create three tasks

Use `POST /tasks` and submit each body separately.

**Task 1**

```json
{
  "title": "Learn Python",
  "description": "Practice functions and loops",
  "completed": false
}
```

**Task 2**

```json
{
  "title": "Learn FastAPI",
  "description": "Practice API development",
  "completed": false
}
```

**Task 3**

```json
{
  "title": "Learn SQL",
  "description": "Practice SELECT queries",
  "completed": false
}
```

If the list and ID counter are fresh, these tasks should receive IDs `1`, `2`, and `3`. If not, use the IDs returned by POST.

### Read all tasks

Call:

```text
GET /tasks
```

Expected result: a JSON list containing all stored tasks.

### Read one task

Call:

```text
GET /tasks/2
```

Expected result: only task `2`.

### Update a task

Call `PUT /tasks/2` and submit:

```json
{
  "title": "Learn FastAPI",
  "description": "CRUD operations completed",
  "completed": true
}
```

Expected result: task `2` has the updated description and `completed` is `true`. Its ID remains `2`.

### Delete a task

Call:

```text
DELETE /tasks/2
```

Expected result:

```json
{
  "message": "Task deleted",
  "id": 2
}
```

Then call `GET /tasks/2` again. It should return `404 Not Found` because task `2` was removed.

---

## 11. Important HTTP Status Codes

| Status code | Meaning | Example |
|---|---|---|
| `200 OK` | Request succeeded | GET, PUT, or our current DELETE endpoint |
| `201 Created` | Resource created successfully | Commonly used for POST |
| `404 Not Found` | Resource doesn't exist | Requesting a missing task ID |
| `422 Unprocessable Entity` | Request data failed validation | A title shorter than the model's minimum length |

FastAPI commonly returns `200` for our current POST endpoint because we haven't configured a different success status code. We can set POST to return `201` when we refine our API design.

---

## 12. Limitations of Our Current Implementation

### In-memory storage isn't persistent
The list is reset when the application process restarts. It also isn't shared across separate application worker processes.

### PUT is a full update
The client must send all the editable fields in the request body. Missing fields may use model defaults, which can unintentionally replace existing values.

### The application has no database yet
The list is useful for learning CRUD logic, but real applications need persistent storage. We'll replace it with PostgreSQL and use SQLAlchemy to interact with the database.

### Response models aren't configured yet
Right now, the API returns the dictionaries we provide. Response models let us define and validate the shape of successful responses; we'll cover those separately.

---

## Quick Revision

- **CRUD:** Create, Read, Update, Delete.
- **POST:** Create a task.
- **GET:** Retrieve tasks.
- **PUT:** Replace the editable fields of an existing task in our implementation.
- **DELETE:** Remove a task.
- **`append()`:** Adds an item to a list.
- **`remove()`:** Removes a matching item from a list.
- **`enumerate()`:** Gives the list position and item while looping.
- **`model_dump()`:** Converts a Pydantic model into a Python dictionary.
- **`**`:** Unpacks dictionary entries into another dictionary.
- **`HTTPException`:** Returns an HTTP error response from an endpoint.
- **`404`:** The requested task doesn't exist.
- **In-memory storage:** Temporary data held in the running application, not persistent database storage.
