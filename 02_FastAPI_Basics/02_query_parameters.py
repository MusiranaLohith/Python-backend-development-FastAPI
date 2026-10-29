from fastapi import FastAPI
from fastapi import Query

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
        if user["city"] == city and user["age"] >= min_age:
            result.append(user)
    return result

users_data1 = [
    {"name": "Lohith", "age": 22, "city": "Hyderabad"},
    {"name": "Rahul", "age": 24, "city": "Bangalore"},
    {"name": "Anu", "age": 21, "city": "Hyderabad"},
    {"name": "Ravi", "age": 25, "city": "Chennai"}
]

@app.get("/user-search")
def search_user(name: str, city: str | None = None):
    result = []
    for user in users_data:
        if user["name"] == name and (user["city"] == city or city is not None):
            result.append(user)
    return result



@app.get("/search-products")
def search_products(name: str = Query(min_length=3, max_length = 20)):
    return {"name":name}


@app.get("/employee-validation")
def employee_validation(
        name: str = Query(min_length=3, max_length=20),
        age: int = Query(ge=18, le=100)
):
    return{
        "name": name,
        "age": age
    }

@app.get("/product-validation")
def product_validation(
        product_name: str = Query(min_length=3, max_length=30),
        price: int = Query(gt=0)
):
    return{
        "product_name": product_name,
        "price": price
    }


@app.get("/product-search")
def product_search(
        name: str = Query(min_length=3, max_length=40, alias = "productName"),
        price: int = Query(gt=0, alias = "productPrice"),
        quantity: int = Query(ge=1,le=100)
):
    return{
        "name": name,
        "price": price,
        "quantity": quantity
    }

@app.get("/product-code-validation")
def product_code_validation(
        product_code: str = Query(pattern= "^[A-Z]{3}[0-9]{3}$")
):
    return{
        "product_code": product_code
    }


@app.get("/employee-search")
def employee_search(
        employee_name: str = Query(min_length=2, max_length=30, alias = "employeeName"),
        age: int = Query(ge=18,le=65),
        department: str | None = Query(None,min_length=2, alias = "dept")
):
    return{
        "Employee Name": employee_name,
        "age": age,
        "department": department
    }



products_data = [
    {"name": "Laptop", "category": "electronics", "price": 75000},
    {"name": "Phone", "category": "electronics", "price": 30000},
    {"name": "Shoes", "category": "fashion", "price": 3000},
    {"name": "Watch", "category": "fashion", "price": 5000}
]


@app.get("/product-filter")
def product_filter(
        category: str = Query(min_length=3),
        max_price: int = Query(gt=0),
        name: str | None = Query(None,min_length=2, alias="productName")
):
    result = []
    for product in products_data:
        if product["category"] == category and product["price"] <= max_price and (name is None or product["name"] == name):
            result.append(product)
    return result


books_data = [
    {"title": "Python Basics", "category": "programming", "price": 500},
    {"title": "FastAPI Guide", "category": "programming", "price": 800},
    {"title": "The Hobbit", "category": "fiction", "price": 600},
    {"title": "Atomic Habits", "category": "selfhelp", "price": 700}
]


@app.get("/book-filter")
def book_filter(
        category: str = Query(min_length=3),
        max_price: int = Query(gt=0),
        title: str | None = Query(None, min_length =3, alias = "bookTitle")
):
    result = []
    for book in books_data:
        if book["category"] == category and book["price"] <= max_price and (title is None or book["title"] == title):
            result.append(book)
    return result



employees_data = [
    {"name": "Lohith", "department": "AI", "age": 22, "salary": 70000},
    {"name": "Rahul", "department": "Backend", "age": 25, "salary": 60000},
    {"name": "Anu", "department": "AI", "age": 21, "salary": 50000},
    {"name": "Ravi", "department": "Frontend", "age": 28, "salary": 80000},
]

@app.get("/employee-directory")
def employee_directory(
        department: str | None = Query(None,min_length=2),
        min_age: int | None = Query(None,ge=18),
        max_salary: int | None = Query(None,gt=0),
        limit: int | None = Query(ge=1,le=4)
):
    result = []
    for employee in employees_data:
        if ((department is None or employee["department"] == department) and
                (min_age is None or employee["age"] >= min_age) and
                (max_salary is None or employee["salary"] <= max_salary) and
                (employee["limit"] == 2 or employee["limit"] == None)):
            result.append(employee)
    return result