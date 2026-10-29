from fastapi import FastAPI, HTTPException

app = FastAPI()

# status-code=200 - Request succeeded
@app.get("/hello")
def hello():
    return {"message": "hello, mate!"}

# status-code=200 - A resource was successfully created
@app.post("/products", status_code=201)
def create_product():
    return {"message" :"Product created"}


@app.post("/tasks", status_code=201)
def tasks():
    return {"message": "Task created successfully"}



@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id != 1:
        raise HTTPException(
            status_code=404,
            detail= "Task Not Found"
        )

    return{
        "id" :1,
        "title" :"Learn FastAPI",
        "completed": False
    }

@app.get("/products/{product_id}")
def product(product_id: int):
    if product_id != 10:
        raise HTTPException(
            status_code=404,
            detail="Task Not Found"
        )

    return{
        "id":10,
        "name": "Keyboard"
    }


students = {
    101: {"id": 101, "name": "Rahul"},
    102: {"id": 102, "name": "Priya"},
    103: {"id": 103, "name": "Arjun"}
}

@app.get("/students/{student_id}")
def student_info(student_id:int):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student Not Found"
        )

    return students[student_id]


employees = {
    201: {"id": 201, "name": "Kiran", "department": "AI"},
    202: {"id": 202, "name": "Meera", "department": "HR"},
    203: {"id": 203, "name": "Dev", "department": "AI"}
}

@app.get("/employees/{employee_id}")
def emp_info(employee_id:int):
    if employee_id not in employees:
        raise HTTPException(
            status_code=404,
            detail = "Employee Not Found"
        )





