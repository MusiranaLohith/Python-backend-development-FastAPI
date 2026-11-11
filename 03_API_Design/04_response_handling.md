
# 04 — Response Handling

## 1. HTTP Response

An HTTP response contains:
- Status code
- Headers
- Response body

FastAPI automatically converts returned Python dictionaries into JSON responses.

## 2. Response class

Import:

```python
from fastapi import Response
```

Used to customize an outgoing response while keeping FastAPI's normal response processing.

Example:

```python
@app.get("/health")
def health(response: Response):
    response.status_code = 200
    response.headers["X-Service"] = "Ticket-API"

    return {"status": "healthy"}
```

Common uses:
- Changing status codes
- Adding custom headers
- Setting cookies

## 3. JSONResponse

Import:

```python
from fastapi.responses import JSONResponse
```

Used to construct and return a JSON HTTP response directly.

Example:

```python
return JSONResponse(
    content={"message": "Ticket created"},
    status_code=201,
    headers={"X-App": "Ticket API"}
)
```

Important difference:

- Returning a normal dictionary allows FastAPI to apply the endpoint's response_model.
- Returning JSONResponse directly bypasses the automatic response_model filtering and serialization.

## 4. response_model vs response_class

### response_model
Defines the structure of the returned data.

```python
@app.get("/tickets", response_model=TicketResponse)
```

### response_class
Defines the response class used for the HTTP response.

```python
@app.get("/status", response_class=HTMLResponse)
```

## 5. HTMLResponse

Import:

```python
from fastapi.responses import HTMLResponse
```

Returns HTML content that the browser renders.

```python
@app.get("/status-page", response_class=HTMLResponse)
def status_page():
    return """
    <html>
        <body>
            <h1>Ticket API is running!</h1>
        </body>
    </html>
    """
```

Content-Type: `text/html`

## 6. PlainTextResponse

Import:

```python
from fastapi.responses import PlainTextResponse
```

Returns plain text without HTML rendering or JSON structure.

```python
@app.get("/plain-message", response_class=PlainTextResponse)
def plain_message():
    return "Ticket successfully created"
```

Content-Type: `text/plain`

## 7. RedirectResponse

Import:

```python
from fastapi.responses import RedirectResponse
```

Redirects the client to another URL.

```python
@app.get("/old-dashboard")
def old_dashboard():
    return RedirectResponse(
        url="/ticket-dashboard",
        status_code=302
    )
```

Common redirect status codes:

| Code | Meaning |
|---|---|
| 301 | Permanent redirect |
| 302 | Temporary redirect |
| 303 | Redirect using GET |
| 307 | Temporary redirect preserving method |
| 308 | Permanent redirect preserving method |

## 8. Important takeaways

- Response: customize a normal outgoing response.
- JSONResponse: construct a JSON response directly.
- HTMLResponse: return HTML.
- PlainTextResponse: return plain text.
- RedirectResponse: redirect the client.
- response_model: define and validate the response data structure.
- response_class: specify the response class.

## 9. Testing

Use Swagger UI:

`http://127.0.0.1:8000/docs`

Also inspect response bodies, status codes and headers in Firefox.
