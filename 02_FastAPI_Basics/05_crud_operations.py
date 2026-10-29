from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class Task(BaseModel):
    title: str = Field(min_length=3)
    description: str | None = "No description"
    completed: bool = False

temp_database = []
next_task_id = 1

@app.post("/tasks")
def create_task(task: Task):
    global next_task_id

    new_task = {
        "id": next_task_id,
        **task.model_dump()
    }

    temp_database.append(new_task)
    next_task_id += 1

    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for index,task in enumerate(temp_database):
        if task["id"] == task_id:
            updated_task_data = {
                "id" : task_id,
                **updated_task.model_dump()
            }

            temp_database[index] = updated_task_data
            return updated_task_data

    raise HTTPException(status_code=404, detail="Task not found")


@app.get("/tasks")
def get_tasks():
    return temp_database


@app.get("/tasks/{task_id}")
def get_task(task_id:int):
    for task in temp_database:
        if task["id"] == task_id:
            return task

    raise HTTPException(status_code=404, detail="Task Not Found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id:int):
    for task in temp_database:
        if task["id"] == task_id:
            temp_database.remove(task)
            return {"message":"Task deleted","id":task_id}

    raise HTTPException(status_code=404, detail="Task not found")