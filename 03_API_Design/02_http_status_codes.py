from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


# 1. HTTP 200 - OK.... Scenario: Successfully retrieve existing data


temp_products = {
    1: {"id": 1, "name": "Laptop", "price": 65000},
    2: {"id": 2, "name": "Mouse", "price": 800}
}


@app.get("/products", status_code=200)
def get_products():
    return temp_products



# 2. HTTP 201 - CREATED,,, Scenario: Successfully create a new resource

class UserCreate(BaseModel):
    name: str
    email: str


temp_users = {}


@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    new_id = len(temp_users) + 1

    temp_users[new_id] = {
        "id": new_id,
        "name": user.name,
        "email": user.email
    }

    return temp_users[new_id]



# 3. HTTP 202 - ACCEPTED... Scenario: Request accepted for processing


@app.post("/reports/generate", status_code=202)
def generate_report():
    return {
        "message": "Report accepted for processing",
        "status": "pending"
    }



# 4. HTTP 204 - NO CONTENT,,,. Scenario: Successfully delete a resource

temp_cart = {
    1: {"id": 1, "name": "Laptop"},
    2: {"id": 2, "name": "Mouse"},
    3: {"id": 3, "name": "Keyboard"}
}


@app.delete("/cart/{product_id}", status_code=204)
def delete_cart_product(product_id: int):
    if product_id not in temp_cart:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    del temp_cart[product_id]
    return None



# 5. HTTP 400 - BAD REQUEST,, Scenario: Application-level validation fails


@app.post("/coupons/apply", status_code=200)
def apply_coupon(coupon: str):

    if coupon != "SAVE10":
        raise HTTPException(
            status_code=400,
            detail="Invalid coupon code"
        )

    return {"message": "Coupon applied successfully"}



# 6. HTTP 401 - UNAUTHORIZED.. Scenario: User is not authenticated


@app.get("/account")
def get_account(is_authenticated: bool = False):

    if not is_authenticated:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    return {"message": "Account information"}



# 7. HTTP 403 - FORBIDDEN... Scenario: User is authenticated but lacks permission


@app.delete("/admin/users/{user_id}")
def delete_user(
    user_id: int,
    is_admin: bool = False
):

    if not is_admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission"
        )

    return {"message": f"User {user_id} deleted"}



#8. HTTP 404 - NOT FOUND

@app.get("/products/{product_id}")
def get_product(product_id: int):

    if product_id not in temp_products:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return temp_products[product_id]



# 9. HTTP 405 - METHOD NOT ALLOWED,,Scenario: Route exists but does not support the method

@app.get("/system/status")
def system_status():
    return {"status": "online"}


# actually fastAPI automatically returns 405.



# 10. HTTP 409 - CONFLICT,, Scenario: New data conflicts with existing data


temp_registered_emails = [
    "user@example.com",
    "admin@example.com"
]


@app.post("/register")
def register(email: str):

    if email in temp_registered_emails:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    temp_registered_emails.append(email)

    return {"message": "Registration successful"}



# 11. HTTP 422 - UNPROCESSABLE CONTENT,,,  Scenario: Request body fails Pydantic validation


class Payment(BaseModel):
    amount: float
    currency: str


@app.post("/payments")
def make_payment(payment: Payment):
    return {
        "message": "Payment request received",
        "amount": payment.amount,
        "currency": payment.currency
    }



# 12. HTTP 500 - INTERNAL SERVER ERROR,,,Scenario: Unexpected server-side error


@app.get("/demo-server-error")
def demo_server_error():

    raise HTTPException(
        status_code=500,
        detail="Internal server error"
    )


# 13. HTTP 503 - SERVICE UNAVAILABLE,,, Service is temporarily unavailable


@app.get("/external-service")
def external_service():

    raise HTTPException(
        status_code=503,
        detail="Service temporarily unavailable"
    )
