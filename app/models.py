from pydantic import BaseModel, Field


class BaseCustomer(BaseModel):
    first_name: str
    last_name: str
    email: str
    gender: str
    company: str
    city: str
    title: str

class Customer(BaseCustomer):
    latitude: float
    longitude: float

class CustomerId(BaseCustomer):
    id: str = Field(..., min_length=1, max_length=99,
                    description="Customer's id")

class Message(BaseModel):
    detail: str
