from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    priority : str

class Task(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

@app.get("/tasks/{task_id}", response_model = TaskResponse)
def get_task(task_id: int):
    return{
        "id" : task_id,
        "title": "Learn FastAPI",
        "description": "Understanding response model",
        "completed": False,
        "admin_note": "This should not appear in the response",
        "priority": "High"
    }

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: Task):
    return{
        "id" : 1,
        **task.model_dump(),
        "priority": "Normal"
    }



class Product(BaseModel):
    name: str = Field(min_length = 3)
    price: float = Field(gt=0)
    in_stock : bool = True

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool

@app.post("/products", response_model = ProductResponse)
def products(product: Product):
    return{
        "id": 101,
        **product.model_dump(),
        "internal_cost": 250
    }