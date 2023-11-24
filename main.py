from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de datos para una persona
class Person(BaseModel):
    name: str
    age: int
    email: str
    id: int
    identification: str
    city: str

# Lista para almacenar personas (simulación de base de datos)
people_db = []

# Operación para crear una persona
@app.post("/persona/", response_model=Person)
def create_person(person: Person):
    people_db.append(person)
    return person

# Operación para obtener todas las personas
@app.get("/persona/", response_model=List[Person])
def get_all_people():
    return people_db

# Operación para obtener una persona por ID
@app.get("/persona/{person_id}", response_model=Person)
def get_person_by_id(person_id: int):
    for person in people_db:
        if person.id == person_id:
            return person
    raise HTTPException(status_code=404, detail="Persona no encontrada")

# Operación para editar una persona por ID
@app.put("/persona/{person_id}", response_model=Person)
def update_person(person_id: int, updated_person: Person):
    for index, person in enumerate(people_db):
        if person.id == person_id:
            people_db[index] = updated_person
            return updated_person
    raise HTTPException(status_code=404, detail="Persona no encontrada")

# Operación para eliminar una persona por ID
@app.delete("/persona/{person_id}", response_model=Person)
def delete_person(person_id: int):
    for index, person in enumerate(people_db):
        if person.id == person_id:
            deleted_person = people_db.pop(index)
            return deleted_person
    raise HTTPException(status_code=404, detail="Persona no encontrada")