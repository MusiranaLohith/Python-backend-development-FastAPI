from fastapi import FastAPI, HTTPException, Path

app = FastAPI()

@app.get("/users/{user_id}/orders/{order_id}")
def get_users(user_id: int, order_id: int):
    return{
        "user_id": user_id,
        "order_id": order_id
    }

students = [
    {"id": 1, "name": "Lohith"},
    {"id": 2, "name": "Rahul"},
    {"id": 3, "name": "Anu"}
]

@app.get("/students/{student_id}")
def students_course(student_id:int):
    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail = "Student not found"
    )


books = [
    {"id": 1, "title": "Python Basics", "price": 500},
    {"id": 2, "title": "FastAPI Guide", "price": 700},
    {"id": 3, "title": "Django Basics", "price": 600}
]

@app.get("/books/{book_id}")
def get_books(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code = 404,
        detail = "Book Not Found"
    )


orders = [
    {"order_id": 101, "customer_id": 1, "amount": 2500},
    {"order_id": 102, "customer_id": 2, "amount": 1800},
    {"order_id": 103, "customer_id": 1, "amount": 4200}
]

@app.get("/customer/{customer_id}/order/{order_id}")
def get_orders(customer_id: int, order_id:int ):
    for order in orders:
        if order["order_id"] == order_id:
          if order["customer_id"] == customer_id:
            return order

        raise HTTPException(
            status_code=404,
            detail="Order not Found"
        )

    raise HTTPException(
        status_code=404,
        detail="Order does not belong to this customer"
    )



@app.get("/products/{product_id}")
def products_ids(product_id:int = Path(
    ge=1,
    description="Unique ID of the product"
)):
    return{
        "Product_id": product_id
    }



bookings = [
    {
        "booking_id": 101,
        "hotel_id": 1,
        "guest_id": 10,
        "room": "Deluxe"
    },
    {
        "booking_id": 102,
        "hotel_id": 1,
        "guest_id": 11,
        "room": "Suite"
    },
    {
        "booking_id": 103,
        "hotel_id": 2,
        "guest_id": 10,
        "room": "Standard"
    }
]

@app.get("/hotels/{hotel_id}/bookings/{booking_id}")
def hostel_booking(hotel_id: int = Path(ge=1), booking_id:int = Path(ge=1)):
    for booking in bookings:
        if booking["booking_id"] == booking_id:
            if booking["hotel_id"] == hotel_id:
                return booking

            raise HTTPException(
                status_code = 404,
                detail = "Booking does not belong to this hotel"
            )

    raise HTTPException(
        status_code = 404,
        detail = "Booking not found"
    )
