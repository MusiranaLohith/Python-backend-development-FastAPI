from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/divide")
def divide_num(a:float ,b:float):
    if b == 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot divide by zero"
        )

    result = a/b
    return {"result" : result}



@app.get("/convert")
def convert_number(value:str):
    try:
        number = int(value)
    except ValueError:
        return {"message": "Pls provide a valid number"}

    return {"number": number}



@app.get("/convert-age")
def convert_age(age:str):
    try:
        age_num = int(age)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Age must be a valid integer"
        )

    return {"age":age_num}


@app.get("/calculate-discount")
def calculate_discount(price:str,discount:str):
    try:
        price_value = float(price)
        discount_value = float(discount)
        discounted_value = price_value - (price_value * discount_value / 100)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Price and discount must be valid numbers"
        )

    return {"Price after discount":discounted_value}




@app.get("/power")
def calculate_power(base: str, exponent:str):
    try:
        base_value=int(base)
        exponent_value=int(exponent)
        power = base_value ** exponent_value
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Base and Exponent must be integers"
        )
    except OverflowError:
        raise HTTPException(
            status_code=400,
            detail="The calculation is too large"
        )

    return {"result": power}



@app.get("/safe-divide")
def safe_divide(a:str, b:str):
    try:
        a1 = float(a)
        b1 = float(b)
        c = a1/b1
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Inputs must be valid numbers"
        )
    except ZeroDivisionError:
        raise HTTPException(
            status_code=400,
            detail="Cannot be divided by zero"
        )
    else:
        return {"divided_value":c}


from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/calculate-average")
def calculate_average(numbers: str):

    try:
        number_list = numbers.split(",")

        values = [float(num) for num in number_list]

        total = sum(values)
        count = len(values)

        average = total / count

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="All values must be valid numbers"
        )

    except ZeroDivisionError:
        raise HTTPException(
            status_code=400,
            detail="Cannot calculate average of an empty list"
        )
    else:
        return {"average": average}

    finally:
        print("Average calculation attempted")


# except Exception
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/general-exception")
def general_exception():

    try:
        number = int("25")
        result = number + "hello"

        return {"result": result}

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid number"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )

