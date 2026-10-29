from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI()
products = []

class Product(BaseModel):
    name: str = Field(min_length = 2)
    price: int = Field(gt=0)
    message: str | None = None


@app.post("/products")
def create_product(product: Product):
    return{
        "name": product.name,
        "price": product.price,
        "message": product.message
    }





class Address(BaseModel):
    city : str
    pincode: int = Field(gt=100000,lt=999999)

class User(BaseModel):
    username: str = Field(min_length = 3)
    age: int = Field(ge=18)
    address: Address
    bio: str | None = "No bio"

@app.post("/users")
def USER(user_data: User):
    return{
        "Name": user_data.username,
        "Age": user_data.age,
        "City": user_data.address.city,
        "Pincode": user_data.address.pincode,
        "Bio": user_data.bio
    }


class Product(BaseModel):
    name : str
    price : int

class Customer(BaseModel):
    name : str
    email : str
@app.post("/orders")
def order_info(prod_specs:Product, customer_data: Customer):
    return{
        "Product-Name": prod_specs.name,
        "Product-price": prod_specs.price,
        "Customer-Name": customer_data.name,
        "Customer-Email" : customer_data.email
    }



class Delivery(BaseModel):
    city : str
    pincode: int
class Customer(BaseModel):
    name: str
    phone_num: str
    delivery : Delivery

@app.post("/delivery")
def customer_delivery(customer_info:Customer):
    return{
        "Name" : customer_info.name,
        "phone_number": customer_info.phone_num,
        "city_name": customer_info.delivery.city,
        "city_pincode": customer_info.delivery.pincode
    }


class Product(BaseModel):
    name: str
    price: int

class Delivery0(BaseModel):
    city : str
    pincode: int

class Customer(BaseModel):
    name: str
    delivery : Delivery0

class Order(BaseModel):
    product : Product
    customer: Customer

@app.post("/order-details")
def order_details(order_details: Order):
    return{
        "product_name": order_details.product.name,
        "product_price": order_details.product.price,
        "customer_name": order_details.customer.name,
        "customer_city": order_details.customer.delivery.city,
        "customer_pincode": order_details.customer.delivery.pincode
    }




