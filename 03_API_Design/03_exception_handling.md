# 03 — Exception Handling in FastAPI

## 1. What is an Exception?

An exception is an event that occurs during program execution and interrupts the normal flow of execution.

Examples:
- `ValueError` — invalid value.
- `TypeError` — incompatible data types.
- `KeyError` — accessing a missing dictionary key.
- `ZeroDivisionError` — division by zero.
- `FileNotFoundError` — requested file doesn't exist.

## 2. Raising HTTP Exceptions

FastAPI provides `HTTPException` to return intentional HTTP error responses.

```python
from fastapi import HTTPException

raise HTTPException(
    status_code=404,
    detail="Resource not found"
)
```

- `raise` interrupts normal execution.
- `status_code` specifies the HTTP status.
- `detail` provides the error message.

FastAPI catches `HTTPException` and sends the corresponding response.

## 3. try and except

- `try`: Executes code that might raise an exception.
- `except`: Handles a matching exception.

```python
try:
    number = int("hello")

except ValueError:
    print("Invalid number")
```

If an exception occurs, the remaining statements in `try` are skipped and the matching `except` executes.

## 4. Multiple except Blocks

Different exceptions can be handled separately.

```python
try:
    number = int("hello")
    result = 100 / number

except ValueError:
    print("Invalid number")

except ZeroDivisionError:
    print("Cannot divide by zero")
```

**Rule: Specific exceptions first, general exceptions last.**

## 5. else Block

Executes only when the `try` block completes without an exception.

```python
try:
    number = int("25")

except ValueError:
    print("Invalid input")

else:
    print("Success")
```

## 6. finally Block

Executes when leaving the exception-handling structure, regardless of whether an exception occurred (except in cases such as forced process termination).

```python
try:
    number = int("hello")

except ValueError:
    print("Invalid input")

finally:
    print("Operation completed")
```

Commonly used for cleanup operations.

## 7. General Exception Handling

`Exception` is a general base class for most ordinary Python exceptions.

```python
try:
    result = 10 / 0

except ZeroDivisionError:
    print("Cannot divide by zero")

except Exception:
    print("Unexpected error")
```

Use specific exception handlers whenever possible. A general handler can act as a fallback for unexpected errors.

In production, log unexpected errors securely and avoid exposing internal details to API clients.

## 8. Combining try/except with HTTPException

```python
@app.get("/convert")
def convert(value: str):
    try:
        number = int(value)

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid number"
        )

    return {"number": number}
```

This converts a Python-level validation failure into an intentional HTTP error response.

## Important distinctions

| Concept | Purpose |
|---|---|
| `raise` | Raises an exception |
| `HTTPException` | Sends an intentional HTTP error response |
| `try` | Attempts potentially failing operations |
| `except` | Handles exceptions |
| `else` | Runs when `try` succeeds |
| `finally` | Runs when leaving the structure |
| `Exception` | General exception base class |

**Production note:** FastAPI already handles unhandled exceptions with a 500 response. Centralized exception handlers and logging are useful for larger applications and will be covered when we build our production-oriented backend.