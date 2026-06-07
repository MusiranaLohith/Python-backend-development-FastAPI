from fastapi import FastAPI
app = FastAPI()

@app.post("/create-user")
def create_user(user: dict):
    return{
        "received_data" : user
    }

@app.post("/create-products")
def create_products(products: dict):
    return{
        "received_products" : products
    }
