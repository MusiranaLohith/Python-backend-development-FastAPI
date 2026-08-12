from fastapi import FastAPI

app = FastAPI()

@app.get("/search")
def search(name: str):
    return{
        "name" : name
    }

@app.get("/products-info")
def products(product_name:str,price: int):
    return{
        "product_name" : product_name,
        "price" : price
    }

@app.get("/users")
def users(name:str,age:int=18,city:str="unknown"):
    return{
        "name": name,
        "age" : age,
        "city" : city
    }

@app.get("/products-details")
def product(name:str,price:int,discount:int=0):
    return{
        "name" : name,
        "price" : price,
        "discount" : discount
    }

books = [
    {"title": "Python Basics", "category": "programming"},
    {"title": "FastAPI Guide", "category": "programming"},
    {"title": "The Hobbit", "category": "fiction"}
]

@app.get("/books")
def get_books(category:str):
    result = []
    for book in books:
        if book["category"] == category:
            result.append(book)
    return result

users_data = [
    {"name": "Lohith", "age": 22, "city": "Hyderabad"},
    {"name": "Rahul", "age": 24, "city": "Bangalore"},
    {"name": "Anu", "age": 21, "city": "Hyderabad"},
    {"name": "Ravi", "age": 25, "city": "Chennai"}
]

@app.get("/users-by-city")
def get_users(city:str):
    result = []
    for user in users_data:
        if user["city"] == city:
            result.append(user)
    return result

@app.get("/users-filtered")
def get_users_data(city:str,min_age:int):
    result = []
    for user in users_data:
        if user["city"] == city and user["age"] <= min_age:
            result.append(user)
    return result
