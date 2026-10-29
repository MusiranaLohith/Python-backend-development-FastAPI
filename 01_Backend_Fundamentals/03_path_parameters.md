# 03 — Path Parameters in FastAPI

## 1. What are Path Parameters?

### Simple definition
Path parameters are values written directly inside a URL that help us identify a specific resource.

**Think of it like this:** If you want to find task number 5, you tell the API which task you want through the URL itself.

```text
/tasks/5
```

Here, `5` is the path parameter.

### Technical definition
A path parameter is a variable part of a URL path that FastAPI extracts from an incoming HTTP request and passes to the corresponding endpoint function.

---

## 2. Our First Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return {"task_id": task_id}
```

Suppose the client requests:

```text
GET /tasks/5
```

The response will be:

```json
{
  "task_id": 5
}
```

### How does this work?

- `@app.get()` tells FastAPI which HTTP method and URL this endpoint handles.
- `/tasks/{task_id}` defines the URL pattern.
- `{task_id}` tells FastAPI that this part of the URL is a variable.
- `task_id: int` means the function expects the value as an integer.
- `return` sends the result back to the client.

**Remember:** The name inside `{}` must match the corresponding function parameter name.

---

## 3. How Does FastAPI Get the Value?

Consider this endpoint:

```python
@app.get("/students/{student_id}")
def get_student(student_id: int):
    return {"student_id": student_id}
```

Now imagine these requests:

| Request URL | Value received by the function |
|---|---|
| `/students/10` | `student_id = 10` |
| `/students/25` | `student_id = 25` |
| `/students/100` | `student_id = 100` |

We don't need to write separate functions for students 10, 25, and 100.

The same function handles all three requests. FastAPI extracts the value from the URL and passes it to the function.

---

## 4. Why Do We Use `task_id: int`?

Look at this line:

```python
def get_task(task_id: int):
```

The `: int` is a Python type annotation.

### Simple definition
It tells Python and FastAPI that `task_id` is expected to be an integer.

### Technical definition
FastAPI uses the type annotation to parse and validate the path parameter against the declared type.

For example:

**Valid request:**

```text
GET /tasks/5
```

FastAPI can convert `5` into the integer `5`.

**Invalid request:**

```text
GET /tasks/hello
```

FastAPI returns a validation error because `"hello"` cannot be parsed as an integer.

You don't need to write your own integer-validation logic for this basic case.

---

## 5. Path Parameters vs Query Parameters

These two concepts look similar, but they serve different purposes.

### Path parameter

```text
/tasks/5
```

Used to identify a specific task.

```python
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return {"task_id": task_id}
```

### Query parameter

```text
/tasks?completed=true
```

Used to filter or modify a collection request.

```python
@app.get("/tasks")
def get_tasks(completed: bool = False):
    return {"completed": completed}
```

In the second example, `completed` is a query parameter because it comes after `?` in the URL.

### Quick comparison

| Feature | Path parameter | Query parameter |
|---|---|---|
| Example | `/tasks/5` | `/tasks?completed=true` |
| Main purpose | Identify a resource | Filter or adjust a request |
| Where it appears | Inside the URL path | After `?` |
| Example variable | `task_id` | `completed` |

**Memory trick:** Path = which resource? Query = what conditions?

---

## 6. How We Used Path Parameters in Our CRUD Project

In `05_crud_operations.py`, we used path parameters to identify individual tasks.

### GET — Retrieve one task

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

When a client requests `/tasks/2`, `task_id` receives `2`. The function searches for the task whose dictionary ID matches that value.

### PUT — Update one task

```python
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    ...
```

The path parameter identifies **which task to update**. The request body supplies **the new task data**.

### DELETE — Delete one task

```python
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    ...
```

The path parameter identifies which task should be removed.

The same idea applies to all three operations: the URL identifies the task, and the endpoint decides what to do with it.

---

## 7. Common Mistakes

### Mistake 1: Parameter names don't match

Incorrect:

```python
@app.get("/tasks/{task_id}")
def get_task(id: int):
    return {"id": id}
```

The URL declares `task_id`, but the function parameter is named `id`.

Correct:

```python
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return {"task_id": task_id}
```

### Mistake 2: Thinking the path parameter automatically finds a database record

This endpoint:

```python
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return {"task_id": task_id}
```

only returns the received ID. It does not search for a real task.

To find a task, we must write the search logic or query a database.

### Mistake 3: Confusing the ID with the list position

Suppose:

```python
temp_database = [
    {"id": 10, "title": "Learn Python"},
    {"id": 25, "title": "Learn FastAPI"}
]
```

Here, task ID `25` is at list index `1`.

- `task_id` is the task's identifier.
- `index` is its position in the list.

They are not necessarily the same.

---

## 8. Quick Revision

- **Path parameter:** A value inside the URL path used to identify a resource.
- **`{task_id}`:** Declares a variable part of the route.
- **`task_id: int`:** Declares the expected type and enables FastAPI validation.
- **`/tasks/5`:** An example of a URL containing a path parameter.
- **Path vs query:** Path identifies a resource; query commonly filters a collection.
- **Important:** Receiving an ID does not automatically retrieve a record. You must implement the search or database query.

