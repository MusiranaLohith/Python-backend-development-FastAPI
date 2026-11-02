from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/divide")
def divide_num(a:float ,b:float):
    if b == 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot divide by zero"
        )

    result = a/b
    return {"result" : result}

