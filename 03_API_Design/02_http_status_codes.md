# 02 — HTTP Status Codes

## 1. What are HTTP Status Codes?

### Simple Definition

Whenever a client (frontend, browser, mobile app) sends a request to a backend API, the server sends back a response.

An HTTP status code tells the client what happened to that request.

For example:
- Did the request succeed?
- Was a new resource created?
- Was the requested data missing?
- Did the server encounter an error?

### Technical Definition

HTTP status codes are three-digit numeric response codes returned by an HTTP server to indicate the outcome of a client's request.

They are grouped into five categories:

| Category | Meaning |
|---|---|
| 1xx | Informational |
| 2xx | Successful |
| 3xx | Redirection |
| 4xx | Client-side errors |
| 5xx | Server-side errors |

---

## 2. Successful Responses (2xx)

These codes indicate that the server successfully handled the request.

### 200 — OK

**Simple meaning:** The request was successful.

**When to use:**
- Retrieving user details.
- Retrieving product information.
- Successfully updating existing data and returning a response.

**FastAPI syntax:**

```python
@app.get("/products", status_code=200)
def get_products():
    return {"message": "Products retrieved"}
```

**Technical definition:** The request has succeeded. The meaning of the response depends on the HTTP method used.

### 201 — Created

**Simple meaning:** The server successfully created something new.

**When to use:**
- Creating a new account.
- Adding a new product.
- Creating a new order.

**FastAPI syntax:**

```python
@app.post("/users", status_code=201)
def create_user():
    return {"message": "User created"}
```

**Technical definition:** The request has been fulfilled and has resulted in the creation of one or more new resources.

### 202 — Accepted

**Simple meaning:** The server accepted the request, but the actual work is not necessarily completed.

**When to use:**
- Accepting a video for compression.
- Accepting a large report-generation request.
- Adding a task to a background processing queue.

**FastAPI syntax:**

```python
@app.post("/reports", status_code=202)
def generate_report():
    return {"message": "Report accepted"}
```

**Technical definition:** The request has been accepted for processing, but the processing has not been completed.

### 204 — No Content

**Simple meaning:** The operation succeeded, but the server has no response content to send.

**When to use:**
- Successfully deleting a cart item.
- Successfully deleting a resource when no confirmation body is required.

**FastAPI syntax:**

```python
@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    return None
```

**Technical definition:** The server successfully fulfilled the request and has no additional response content to send.

**Important:** A 204 response must not contain a response body.

### Important Differences

| Code | Remember it as |
|---|---|
| 200 | Operation successful |
| 201 | New resource created |
| 202 | Request accepted, processing pending |
| 204 | Operation successful, no response body |

---

## 3. Client Errors (4xx)

These codes indicate that the server cannot fulfil the request because of something related to the client's request, authentication, permissions or requested resource.

### 400 — Bad Request

**Simple meaning:** The client sent an invalid or malformed request.

**When to use:**
- Invalid request syntax.
- Invalid or unacceptable request parameters.
- An application-specific request rule fails.

**FastAPI syntax:**

```python
from fastapi import HTTPException

@app.post("/coupons")
def apply_coupon(coupon: str):

    if coupon != "SAVE10":
        raise HTTPException(
            status_code=400,
            detail="Invalid coupon code"
        )

    return {"message": "Coupon applied"}
```

**Technical definition:** The server cannot or will not process the request because of a perceived client error.

### 401 — Unauthorized

**Simple meaning:** The server cannot verify the user's identity.

**When to use:**
- User hasn't logged in.
- Authentication token is missing.
- Authentication token is invalid or expired.

**FastAPI syntax (simplified demonstration):**

```python
@app.get("/account")
def get_account(is_authenticated: bool = False):

    if not is_authenticated:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    return {"message": "Account details"}
```

**Technical definition:** The request lacks valid authentication credentials for the target resource.

### 403 — Forbidden

**Simple meaning:** The server knows who the user is, but the user doesn't have permission to perform the requested action.

**When to use:**
- Normal employee attempts to access an admin-only page.
- User tries to delete another user's account without permission.

**FastAPI syntax (simplified demonstration):**

```python
@app.delete("/admin/users/{user_id}")
def delete_user(user_id: int, is_admin: bool = False):

    if not is_admin:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )

    return {"message": "User deleted"}
```

**Technical definition:** The server understood the request but refuses to fulfil it because the client does not have the necessary permissions.

### 404 — Not Found

**Simple meaning:** The requested resource doesn't exist.

**When to use:**
- Product ID doesn't exist.
- Requested user doesn't exist.
- Order number cannot be found.

**FastAPI syntax:**

```python
@app.get("/products/{product_id}")
def get_product(product_id: int):

    if product_id not in products:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return products[product_id]
```

**Technical definition:** The origin server cannot find a current representation for the target resource or is unwilling to disclose that one exists.

### 405 — Method Not Allowed

**Simple meaning:** The endpoint exists, but it doesn't support the HTTP method used by the client.

**Example:**

```python
@app.get("/employees")
def get_employees():
    return {"message": "Employee list"}
```

If the client sends:

```http
DELETE /employees
```

FastAPI automatically returns 405 because this endpoint supports GET, not DELETE.

**Technical definition:** The request method is known to the server but is not supported by the target resource.

### 409 — Conflict

**Simple meaning:** The request conflicts with the current state of existing data.

**When to use:**
- Registering with an email that already exists.
- Attempting to create a duplicate resource.
- Trying to update data in a way that conflicts with its current state.

**FastAPI syntax:**

```python
@app.post("/register")
def register(email: str):

    if email in registered_emails:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    registered_emails.append(email)

    return {"message": "Registration successful"}
```

**Technical definition:** The request could not be completed because it conflicts with the current state of the target resource.

### 422 — Unprocessable Content

**Simple meaning:** The server understands the request, but the submitted content fails validation or cannot be processed according to the application's requirements.

**When to use:**
- Sending text where a number is expected.
- Missing a required field in a request body.
- Sending data that fails Pydantic validation.

**FastAPI syntax:**

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int


@app.post("/users")
def create_user(user: User):
    return {
        "name": user.name,
        "age": user.age
    }
```

If the client sends:

```json
{
    "name": "Lohith",
    "age": "twenty"
}
```

FastAPI automatically returns 422 because `age` must be an integer.

**Technical definition:** The server understands the content type and syntax of the request, but cannot process the contained instructions because of semantic errors.

### Important Differences

**401 vs 403**

- 401 → Authentication failed or is missing.
- 403 → Authentication may be successful, but permission is insufficient.

**400 vs 422**

- 400 → General client request error.
- 422 → Request content fails validation or semantic requirements.

**404 vs 405**

- 404 → Resource or endpoint not found.
- 405 → Endpoint exists, but the HTTP method isn't supported.

**409 vs 400**

- 400 → Invalid request.
- 409 → Conflict with existing resource state.

---

## 4. Server Errors (5xx)

These codes indicate that the server failed to fulfil a request.

### 500 — Internal Server Error

**Simple meaning:** Something unexpected went wrong inside the backend.

**When to use:**
- Unexpected programming error.
- Unhandled exception.
- Unexpected internal processing failure.

**FastAPI syntax:**

```python
@app.get("/demo-error")
def demo_error():

    raise HTTPException(
        status_code=500,
        detail="Internal server error"
    )
```

**Technical definition:** The server encountered an unexpected condition that prevented it from fulfilling the request.

### 503 — Service Unavailable

**Simple meaning:** The service is temporarily unable to handle requests.

**When to use:**
- Server maintenance.
- Temporary service outage.
- Server overload.
- A required external dependency is temporarily unavailable.

**FastAPI syntax:**

```python
@app.get("/external-service")
def external_service():

    raise HTTPException(
        status_code=503,
        detail="Service temporarily unavailable"
    )
```

**Technical definition:** The server is currently unable to handle the request due to temporary overload or scheduled maintenance, which is likely to be alleviated after some delay.

### Important Difference: 500 vs 503

- 500 → Unexpected internal server failure.
- 503 → Temporary service unavailability.

---

## 5. Complete Status Code Reference

| Status Code | Name | Main Purpose |
|---|---|---|
| 200 | OK | Successful operation |
| 201 | Created | New resource created |
| 202 | Accepted | Request accepted for processing |
| 204 | No Content | Success without response body |
| 400 | Bad Request | Invalid client request |
| 401 | Unauthorized | Authentication failure |
| 403 | Forbidden | Insufficient permission |
| 404 | Not Found | Resource not found |
| 405 | Method Not Allowed | Unsupported HTTP method |
| 409 | Conflict | Conflict with existing data |
| 422 | Unprocessable Content | Validation or semantic error |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Temporary service outage |

---

## 6. Important FastAPI Concepts

### HTTPException

`HTTPException` allows us to stop normal execution of an endpoint and return an HTTP error response.

Syntax:

```python
raise HTTPException(
    status_code=404,
    detail="Resource not found"
)
```

- `status_code` specifies the HTTP response status.
- `detail` provides information about the error.

### Automatic Status Codes in FastAPI

FastAPI automatically handles certain errors.

| Situation | Automatic response |
|---|---|
| Request body fails Pydantic validation | 422 |
| Required query parameter is missing | 422 |
| Request uses an unsupported method | 405 |

We don't need to manually write `HTTPException` for these standard framework-handled cases.

### Important Learning Note

The examples in this chapter demonstrate HTTP status-code selection. Some use simplified in-memory data and flags for learning purposes.

For example, `is_authenticated=True` is not real authentication. Actual authentication and authorization require proper security mechanisms, which we'll study later.

---

## 7. Final Technical Summary

HTTP status codes are an essential part of API design because they allow clients to understand the outcome of their requests.

When designing or reviewing an API, the developer must select a status code that accurately represents what happened.

The same endpoint may return different status codes depending on the result of the operation.

**Remember:** A successful HTTP response does not always mean 200, and an error response should describe the actual reason the request failed.