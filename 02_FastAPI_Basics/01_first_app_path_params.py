from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def home():
    return{
        "message" : "Hello.."
    }

@app.get("/about")
def about():
    return{
        "message": "This is my FastAPI backend"
    }

@app.get("/users")
def users():
    return{
        "users": ["Lohith", "Rahul", "Anu"]
    }

@app.get("/status")
def status():
    return{
        "status": "running"
    }

# path params
@app.get("/users/{user_id}")
def get_user(user_id:int):
    return{
        "user_id" : user_id
    }

@app.get("/products/{product_id}")
def get_product_id(product_id:int):
    return{
        "product_id" : product_id,
        "product_name" : "Laptop"
    }

@app.get("/products/{product_id}/{quantity}")
def product_details(product_id:int, quantity:int):
    return{
        "product_id" : product_id,
        "quantity" : quantity,
        "total_quantity" : product_id * quantity
    }

@app.get("/students/{student_id}/courses/{course_id}")
def get_details(student_id:int,course_id:int):
    return{
        "student_id" : student_id,
        "course_id" : course_id
    }

@app.get("/students/{student_id}")
def get_name_id(student_id:int):
    if student_id == 1:
        return{
            "student_id" : student_id,
            "name" : "Lohith"
        }
    elif student_id == 2:
        return{
            "student_id": student_id,
            "name" : "Rahul"
        }
    elif student_id == 3:
        return{
            "student_id": student_id,
            "name" : "Anu"
        }
    else:
        return{
            "message" : "Student Not FOund"
        }

@app.get("/users/{user_id}/orders/{order_id}")
def order_details(user_id:int, order_id:int):
    return{
        "user_id" : user_id,
        "order_id" : order_id,
        "message" : f"Order belongs to user {user_id}"
    }