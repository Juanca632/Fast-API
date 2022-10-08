
#Python
from doctest import Example
from importlib.resources import path
from lib2to3.pytree import Base
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field, EmailStr

#FastAPI
from fastapi import FastAPI, Query
from fastapi import Body, Path, status, Form, Header, Cookie

app = FastAPI()

#Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class PersonBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, example="Miguel")
    last_name: str = Field(..., min_length=1, max_length=50, example="Torres")
    age: int = Field(..., gt=0, le=115, example=25)
    hair_color: Optional[HairColor] = Field(default=None, example="black")
    is_married: Optional[bool] = Field(default=None, example=False)

class Person(PersonBase):
    password: str = Field(..., min_length=8)

        #class Config:
        #    schema_extra = {
        #        "example": {
        #            "first_name": "Facundo",
        #            "last_name": "Garcia Martoni",
        #            "age": 21,
        #            "hair_color": "blonde",
        #            "is_married": False
        #        }
        #    }

class PersonOut(PersonBase):
    pass

class Location(BaseModel):  
    city: str
    state: str
    country: str

class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="juanca632")

@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {"Hello": "World"}

#request and response body
@app.post("/person/new", response_model=PersonOut, status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body(...)):
    return person

#Validaciones: Query parameters
@app.get("/person/detail", status_code=status.HTTP_200_OK)
def show_person(
    name: Optional[str] = Query(None, min_length=1,max_length=50,title="Person Name",description="This is the person name. It's between 1 and 50 characters", example="Rocío"),
    age: int = Query(..., title="Person Age", description="This is the person age. It's required", example=25)
):
    return {name: age}

#Validaciones: path parameters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(..., gt=0, title="Person ID", description="This is the person ID. It's required", example=123)
):
    return {person_id: "It exist"}

#validaciones: Request body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(..., gt=0, title="Person ID", description="This is the person ID. It's required", example=123),

    person: Person = Body(...),
    #location: Location = Body(...)
):
    #results = person.dict()
    #results.update(location.dict())
    #return results
    return person

@app.post("/login", response_model=LoginOut, status_code=status.HTTP_200_OK)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

#Cookies and headers parameters
@app.post("/contact", status_code=status.HTTP_200_OK)
def contact(
    first_name: str = Form(...,max_length=20,min_length=1),
    last_name: str = Form(...,max_length=20,min_length=1),
    email: EmailStr = Form(...),
    message: str = Form(...,min_length=20),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
    ):
    return user_agent