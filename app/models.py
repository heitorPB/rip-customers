from pydantic import BaseModel

class Customer(BaseModel):
    first_name: str
    last_name: str
    email: str
    gender: str
    company: str
    city: str
    title: str


class Message(BaseModel):
    detail: str
