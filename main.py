from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Datos de ejemplo para personas
personas = [
    {"id": 1, "nombre": "Juan", "edad": 30},
    {"id": 2, "nombre": "María", "edad": 25},
    {"id": 3, "nombre": "Pedro", "edad": 35},
]

# Ruta para listar todas las personas
@app.get("/personas")
async def listar_personas():
    return personas

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
