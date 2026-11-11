from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse


app = FastAPI()

# Response

@app.get("/normal-response")
def normal_response(response: Response):

    response.status_code = 201
    response.headers["X-App-Version"] = "1.0"
    response.headers["X-Environment"] = "Development"

    return{
        "message" : "Hello from FastAPI",
        "status": "working"
    }


@app.get("/health")
def health_info(response: Response):

    response.status_code = 200
    response.headers["X-Service"] = "Ticket-Management"
    response.headers["X-Version"] = "1.0"

    return{
        "status": "healthy",
        "database" : "connected"
    }



class ticket(BaseModel):
    title: str
    description: str
    priority: str

@app.post("/tickets/ticket_id")
def ticket_info(Ticket:ticket,ticket_id:int,response: Response):

    response.status_code = 201
    response.headers["X-API-Version"] = "1.0"
    response.headers["Location"] = f"/tickets/{ticket_id}"
    return{
        "ticket_id": ticket_id,
        "title": Ticket.title,
        "description": Ticket.description,
        "priority": Ticket.priority,
        "status":"open"
    }



#JSONResponse

@app.get("/ticket-json")
def get_ticket_json():
    ticket={
        "ticket_id" :1042,
        "status" : "open",
        "message" : "Ticket retrieved successfully"
    }

    return JSONResponse(
        content=ticket,
        status_code= 202,
        headers={
            "X-Request-Type": "custom"
        }
    )




class TicketResponse(BaseModel):
    ticket_id: int
    message: str


@app.get("/response-example", response_model=TicketResponse)
def response_example(response: Response):
    response.status_code = 201

    return {
        "ticket_id": 1042,
        "message": "Ticket created",
        "internal_note": "Only for developers"
    }


@app.get("/json-response-example", response_model=TicketResponse)
def json_response_example():
    return JSONResponse(
        content={
            "ticket_id": 1042,
            "message": "Ticket created",
            "internal_note": "Only for developers"
        },
        status_code=201
    )


# HTMLResponse
@app.get("/status-page", response_class=HTMLResponse)
def status_page():
    return """
    <html>
        <head>
            <title>Ticket API</title>
        </head>
        <body>
            <h1>Ticket API is running!</html>
            <p>All system operational.</p>
        </body>
    </html>
    """


@app.get("/ticket-dashboard", response_class=HTMLResponse)
def ticket_dashboard():
    return """
    <html>
        <body>
            <h1>Ticket Dashboard</h1>

            <h2>Ticket Statistics</h2>

            <p>Open Tickets: 24</p>
            <p>Closed Tickets: 86</p>
            <p>Pending Tickets: 12</p>
        </body>
    </html>
    """


@app.get("/ticket-details", response_class=HTMLResponse)
def ticket_details():
    return """
    <html>
        <body>
            <h1>Ticket #1042</h1>
            <p><b>Title:</b> VPN not working</p>
            <p><b>Priority:</b> High</p>
            <p><b>Status:</b> Open</p>
            <p><b>Assigned Engineer:</b> Ravi</p>
        </body>
    </html>
    """



# PlainTextResponse
from fastapi.responses import PlainTextResponse

@app.get("/plain-message", response_class=PlainTextResponse)
def plain_message():
    return "Ticket successfully created"


from fastapi.responses import PlainTextResponse

@app.get("/health-text", response_class=PlainTextResponse)
def health_text():
    return "Ticket API is healthy"


@app.get("/database-status", response_class=PlainTextResponse)
def database_status():
    return "Database connection failed"



# RedirectResponse
@app.get("/old-dashboard")
def old_dashboard():
    return RedirectResponse(url="/ticket-dashboard")


@app.get("/login-success")
def login_success():
    return RedirectResponse(url="/ticket-dashboard")


@app.get("/legacy-tickets")
def legacy_tickets():
    return RedirectResponse(url="/ticket-dashboard")


@app.get("/old-system")
def old_school():
    return RedirectResponse(url="/ticket-dashboard")


@app.get("/temporary-dashboard")
def temporary_dashboard():
    return RedirectResponse(
        url = "/ticket-dashboard",
        status_code=302
    )

@app.get("/old-support")
def old_support():
    return RedirectResponse(
        url="/ticket-dashboard",
        status_code=301
    )


@app.post("/ticket-submitted")
def ticket_submitted():
    return RedirectResponse(
        url="/ticket-dashboard",
        status_code=303
    )
