# Response Models in FastAPI

## 1. Simple Definition

A **response model** defines the structure of the data an API sends back to the client.

It specifies which fields should appear in the response and what types those fields should have.

For example, an application may store internal information about a product, but the API should expose only its ID, name, price, and availability.

## 2. Technical Definition

In FastAPI, a response model is typically a Pydantic model specified using the `response_model` parameter of a path operation decorator.

FastAPI uses the model to validate the returned data, serialize it into the response format, and filter out fields that are not part of the declared response schema.

If the returned data violates the response model, FastAPI normally raises a response-validation error, resulting in HTTP 500.

## 3. Defining a Response Model

```python
from pydantic import BaseModel


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
```

Explanation:

- `BaseModel` is the base class used to define a Pydantic model.
- `id: int` declares an integer field.
- `title: str` declares a string field.
- `description: str | None` allows a string or `None`.
- `completed: bool` declares a Boolean field.

The `description` field allows `None`, but it is still required when constructing this model unless a default value is provided.

## 4. Using `response_model`

```python
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    return {
        "id": task_id,
        "title": "Learn FastAPI",
        "description": "Understanding response models",
        "completed": False,
        "admin_note": "Internal information"
    }
```

Here:

- `@app.get()` registers a GET endpoint.
- `response_model=TaskResponse` declares the outgoing response schema.
- `get_task()` returns a Python dictionary.
- FastAPI applies the response model before sending the response to the client.

The client receives:

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": "Understanding response models",
  "completed": false
}
```

The `admin_note` field is excluded because it is not part of `TaskResponse`.

**Important:** An extra field in the returned dictionary is normally filtered out; it does not automatically cause a validation error.

## 5. Response Filtering

Suppose the endpoint returns:

```python
return {
    "id": 101,
    "name": "Keyboard",
    "price": 799.0,
    "in_stock": True,
    "internal_cost": 250
}
```

And the response model is:

```python
class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool
```

The client receives:

```json
{
  "id": 101,
  "name": "Keyboard",
  "price": 799.0,
  "in_stock": true
}
```

The `internal_cost` field is filtered out.

This is useful for controlling the public response structure. It is not a substitute for authentication, authorization, or careful handling of sensitive data.

## 6. Response Validation

A response model also checks whether returned data matches the declared schema.

For example:

```python
class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool
```

If the endpoint returns data that cannot be validated against this model, FastAPI normally raises a response-validation error.

A response-validation failure generally results in HTTP 500 because the server produced an invalid response.

This differs from request validation:

- Invalid incoming request data generally produces HTTP 422.
- Invalid outgoing response data generally produces HTTP 500.

For example, the following response value violates a string field:

```python
"priority": 123
```

when the response model declares:

```python
priority: str
```

The result is a response-validation failure in the normal FastAPI setup.

## 7. Request Models Versus Response Models

Request models and response models have different responsibilities.

| Request model | Response model |
|---|---|
| Describes incoming data | Describes outgoing data |
| Validates client input | Validates and shapes server output |
| Used as an endpoint parameter | Used through `response_model` or an appropriate return annotation |
| May omit server-generated fields | May include server-generated fields |

For example:

```python
class Task(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    priority: str
```

The client supplies the task's editable fields. The server supplies the ID and priority.

Separate models allow the API to accept one structure and return another.

## 8. Request Defaults

In the request model:

```python
class Task(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False
```

A client can send:

```json
{
  "title": "Learn SQLAlchemy"
}
```

Pydantic supplies the default values:

- `description` becomes `None`.
- `completed` becomes `False`.

When returned through a response model that includes both fields, these values appear as JSON `null` and `false`, respectively.

A supplied value overrides the default.

## 9. A Complete Example

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Product(BaseModel):
    name: str = Field(min_length=3)
    price: float = Field(gt=0)
    in_stock: bool = True


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool


@app.post("/products", response_model=ProductResponse)
def products(product: Product):
    return {
        "id": 101,
        **product.model_dump(),
        "internal_cost": 250
    }
```

### How it works

1. The client sends JSON to `POST /products`.
2. FastAPI validates the request using `Product`.
3. The validated Pydantic object is passed to the `product` parameter.
4. `product.model_dump()` converts the model into a Python dictionary.
5. Dictionary unpacking with `**` inserts the product fields into the returned dictionary.
6. The endpoint adds a hardcoded ID.
7. FastAPI applies `ProductResponse` and filters out `internal_cost`.
8. The client receives the resulting JSON response.

### Example request

```json
{
  "name": "Keyboard",
  "price": 799.0
}
```

### Example response

```json
{
  "id": 101,
  "name": "Keyboard",
  "price": 799.0,
  "in_stock": true
}
```

### Validation constraints

- `Field(min_length=3)` requires the product name to contain at least three characters.
- `Field(gt=0)` requires the price to be greater than zero.
- `in_stock: bool = True` provides a default availability value.

Invalid names or prices produce request-validation errors, normally with HTTP 422.

**Note:** This is a demonstration endpoint. The ID is hardcoded, and the product is not stored in a database. Persistent storage will be implemented when we integrate PostgreSQL.

## 10. Common Mistakes

1. **Confusing request and response models:** A request model validates incoming data; a response model defines outgoing data.

2. **Passing `BaseModel` directly:** Use your specific model class, such as `ProductResponse`, rather than `BaseModel` itself.

3. **Assuming extra fields cause errors:** Extra fields in returned data are normally filtered out by a response model.

4. **Assuming response models store data:** They validate and shape responses; they do not save records to a database.

5. **Assuming `str | None` automatically makes a field omittable:** A default value is needed if the field should be optional to omit during model construction.

6. **Returning hardcoded data unintentionally:** An endpoint can accept a validated request but still ignore it if it returns fixed values.

7. **Treating response validation as complete security:** Sensitive information should be protected through appropriate data handling and access controls as well.

## Quick Revision Summary

- A response model defines the structure of outgoing API data.
- Pydantic models inherit from `BaseModel`.
- `response_model=ProductResponse` tells FastAPI how to validate and shape the response.
- Request models validate incoming data.
- Response models validate and filter outgoing data.
- Separate request and response models are useful when server-generated or internal fields differ from client-supplied fields.
- Request validation failures generally return HTTP 422.
- Response validation failures generally return HTTP 500.
- `model_dump()` converts a Pydantic model into a Python dictionary.
- Response models do not persist data.
