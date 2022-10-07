
#Python
from importlib.resources import path
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI, Query
from fastapi import Body, Path

app = FastAPI()

#Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

class Location(BaseModel):
    city: str
    state: str
    country: str

@app.get("/")
def home():
    return {"Hello": "World"}

#request and response body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

#Validaciones: Query parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(None, min_length=1,max_length=50,title="Person Name",description="This is the person name. It's between 1 and 50 characters"),
    age: int = Query(..., title="Person Age", description="This is the person age. It's required")
):
    return {name: age}

#Validaciones: path parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(..., gt=0, title="Person ID", description="This is the person ID. It's required")
):
    return {person_id: "It exist"}

#validaciones: Request body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(..., gt=0, title="Person ID", description="This is the person ID. It's required"),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results