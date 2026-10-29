# 04 — Request Bodies in FastAPI

## 1. What is a Request Body?

### Simple definition
A request body is the data a client sends to an API.

**Think of it like this:** When you create a task, you need to tell the API the task's title, description, and completion status. That information is sent in the request body.

Example request body:

```json
{
  "title": "Learn FastAPI",
  "description": "Practice request bodies",
  "completed": false
}
```

### Technical definition
A request body is data included in an HTTP request, commonly used to send structured information to a server. FastAPI can parse JSON request bodies and validate them using a Pydantic model.

---

## 2. What is Pydantic?

### Simple definition
Pydantic helps us check whether incoming data has the expected structure and types.

**Think of it like a security checkpoint:** Before accepting a task, the API checks whether the submitted data meets the rules.

### Technical definition
Pydantic is a Python library for data validation and parsing. It uses Python type annotations and model definitions to validate incoming data and create model instances.

We import the tools we need:

```python
from pydantic import BaseModel, Field
```

- `BaseModel` lets us define a data model.
- `Field` lets us add extra validation rules or configuration to a field.

---

## 3. What is `BaseModel`?

### Simple definition
`BaseModel` lets us define what fields an object should contain and what types those fields should have.

### Technical definition
A Pydantic `BaseModel` subclass defines a schema used to parse and validate data, producing a model instance with validated fields.

Example:

```python
from pydantic import BaseModel

class Task(BaseModel):
    title: str
    completed: bool
```

This model defines two fields:

- `title` must be a string.
- `completed` must be a Boolean (`True` or `False`).

For example, this input follows the model:

```json
{
  "title": "Learn Python",
  "completed": false
}
```

But if `title` is missing, or its value cannot be validated as a string, Pydantic validation can reject the input.

---

## 4. Understanding Our `Task` Model

This is the model we used in `05_crud_operations.py`:

```python
class Task(BaseModel):
    title: str = Field(min_length=3)
    description: str | None = "No description"
    completed: bool = False
```

Let's understand each line.

### `title: str = Field(min_length=3)`

**Simple meaning:** The title must be a string containing at least three characters.

**Technical meaning:** The field is typed as `str`, with a minimum-length constraint of three characters.

Valid:

```json
{
  "title": "Python"
}
```

Invalid:

```json
{
  "title": "AI"
}
```

The second example fails because `"AI"` has only two characters.

### `description: str | None = "No description"`

**Simple meaning:** The description can be text or `None`. If the client leaves it out, it defaults to `"No description"`.

**Technical meaning:** `str | None` is a union type allowing either a string or `None`. The assigned default makes the field optional in the input.

For example, if the client sends:

```json
{
  "title": "Learn FastAPI"
}
```

The model supplies the default description:

```python
"No description"
```

Important distinction: `str | None` allows `None`, while the default value determines what happens when the field is omitted.

### `completed: bool = False`

**Simple meaning:** The task's completion status is a Boolean. If the client does not provide it, the task starts as incomplete.

**Technical meaning:** The field uses the `bool` type and has a default value of `False`.

If the client sends:

```json
{
  "title": "Learn FastAPI"
}
```

Then `completed` defaults to `False`.

---

## 5. How FastAPI Receives a Request Body

Consider this endpoint:

```python
@app.post("/tasks")
def create_task(task: Task):
    return task
```

Suppose the client sends this JSON body:

```json
{
  "title": "Learn Python",
  "description": "Practice functions",
  "completed": false
}
```

Here's what happens:

1. The client sends the request to `POST /tasks`.
2. FastAPI reads the JSON body.
3. FastAPI uses the `Task` model to validate the data.
4. If validation succeeds, FastAPI passes a `Task` model instance into the function as `task`.
5. The function returns that model, and FastAPI creates the HTTP response.

**Key idea:** `task` is the variable holding the validated model instance. It isn't the original JSON text.

---

## 6. What Is `model_dump()`?

### Simple definition
`model_dump()` converts a Pydantic model into a regular Python dictionary.

### Technical definition
`model_dump()` serializes a Pydantic model into a Python dictionary, using the model's configured serialization rules.

Example:

```python
task_data = task.model_dump()
```

If `task` contains:

```python
title = "Learn Python"
description = "Practice functions"
completed = False
```

Then `task.model_dump()` produces:

```python
{
    "title": "Learn Python",
    "description": "Practice functions",
    "completed": False
}
```

Important: `model_dump()` produces a **Python dictionary**, not a JSON string.

Python uses `False` and `True`; JSON uses `false` and `true`.

---

## 7. What Does `**` Mean in a Dictionary?

### Simple definition
Inside a dictionary literal, `**` unpacks another dictionary's key-value pairs into the new dictionary.

### Technical definition
Dictionary unpacking with `**` merges the entries of a mapping into a dictionary display.

Example:

```python
task_details = {
    "title": "Learn Python",
    "completed": False
}

new_task = {
    "id": 1,
    **task_details
}
```

Result:

```python
{
    "id": 1,
    "title": "Learn Python",
    "completed": False
}
```

The `id` is added directly, and the fields from `task_details` are unpacked into the same dictionary.

This is the same idea used in our project:

```python
new_task = {
    "id": next_task_id,
    **task.model_dump()
}
```

The server generates the ID, while the model supplies the task fields.

---

## 8. Request Body vs Path Parameter

These serve different purposes.

### Path parameter

```text
/tasks/5
```

Identifies which task the request refers to.

```python
def get_task(task_id: int):
    ...
```

Here, `task_id` comes from the URL.

### Request body

```json
{
  "title": "Learn FastAPI",
  "description": "Practice APIs",
  "completed": false
}
```

Supplies structured data to the API.

```python
def create_task(task: Task):
    ...
```

Here, `task` comes from the validated request body.

**Memory trick:** The URL tells us which resource; the request body supplies the data.

---

## 9. How This Connects to Our CRUD Project

In our task API:

- **POST:** Receives a `Task` model and creates a task.
- **GET:** Usually retrieves stored task data; it may not need a request body.
- **PUT:** Receives the task ID from the URL and the updated fields through a `Task` request body.
- **DELETE:** Receives the task ID from the URL and removes the matching task; it doesn't need a request body in our implementation.

The `Task` model describes the incoming task data. It doesn't automatically store tasks in a database. Our current application stores them in the Python list `temp_database`.

---

## 10. Common Mistakes

### Mistake 1: Thinking `model_dump()` creates JSON

It returns a Python dictionary. FastAPI handles converting supported return values to JSON for HTTP responses.

### Mistake 2: Thinking `task` is a dictionary

In this function:

```python
def create_task(task: Task):
    ...
```

`task` is a Pydantic model instance. Use `task.title` to access a field, or `task.model_dump()` to convert it into a dictionary.

### Mistake 3: Thinking defaults make every field nullable

A default value lets a field be omitted from the input. It doesn't necessarily mean the field accepts `None`.

For example, `completed: bool = False` has a default, but `None` is not a valid Boolean value under normal strict interpretation of the model's type.

### Mistake 4: Expecting Pydantic to save data

Pydantic validates and parses data. Your endpoint must still decide what to do with that data, such as adding it to a list or saving it to PostgreSQL.

---

## Quick Revision

- **Request body:** Data sent by a client in an HTTP request.
- **Pydantic:** Library for validating and parsing data.
- **`BaseModel`:** Base class used to define data models.
- **`Field`:** Adds field constraints or configuration.
- **`model_dump()`:** Converts a Pydantic model to a Python dictionary.
- **`**some_dict`:** Unpacks dictionary entries into another dictionary.
- **Defaults:** Supply values when fields are omitted.
- **Validation:** Checks whether input matches the model's declared rules.
