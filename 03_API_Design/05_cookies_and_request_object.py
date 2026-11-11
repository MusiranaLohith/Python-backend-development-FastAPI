from fastapi import FastAPI, Response, Cookie

app = FastAPI()

@app.post("/login")
def login(response: Response):

    response.set_cookie(
        key="session_id",
        value="user_session_1042",
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=3600
    )
    return{
        "message": "Login Successful"
    }


@app.get("/session")
def read_session(session_id: str | None = Cookie(default=None)):
    if session_id is None:
        return{
            "message" : "No session cookie found"
        }
    return{
        "message" : "Session cookie received",
        "session_id": session_id
    }


