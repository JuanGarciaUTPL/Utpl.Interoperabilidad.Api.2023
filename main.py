from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

#libreria para generar un id unico
import uuid

#importar librerias para el manejo de la base de datos pymongo
import pymongo

#configuracion de mongo
cliente = pymongo.MongoClient("mongodb+srv://utplinteroperabilidad:0b1Fd3PFZZInSuZK@cluster0.susnphb.mongodb.net/?retryWrites=true&w=majority")
database = cliente["directorio"]
coleccion = database["persona"]

app = FastAPI(
    title="API de personas del segundo parcial",
    description="API para el manejo de personas en el segundo parcial de la materia de Interoperabilidad",
    version="1.0.1",
    contact={
        "name": "Felipe Quiñonez",
        "email": "fdquinones@utpl.edu.ec",
        "url": "https://github.com/fdquinones/Utpl.Interoperabilidad.Api"
    },
    license_info={
        "name": "MIT License",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
    openapi_tags=[
        {
            "name": "Persona",
            "description": "Operaciones para el manejo de personas"
        }
    ]
)

# Modelo de datos para una persona
class PersonDto(BaseModel):
    name: str
    age: int
    email: str
    identification: str
    city: str

# Modelo de datos para una persona con ID, para conectar con la base de datos
class PersonRepository(BaseModel):
    name: str
    age: int
    email: str
    identification: str
    city: str
    id: str

# Lista para almacenar personas (simulación de base de datos)
people_db = []

# Operación para crear una persona
@app.post("/persona/", response_model=PersonRepository, tags=["Persona"])
def create_person(personInput: PersonDto):
    idPerson = str(uuid.uuid4())
    itemPersona = PersonRepository(name=personInput.name, age=personInput.age, email=personInput.email, identification=personInput.identification, city=personInput.city, id=idPerson)
    result = coleccion.insert_one(itemPersona.dict())
    return itemPersona

# Operación para obtener todas las personas
@app.get("/persona/", response_model=List[PersonRepository], tags=["Persona"])
def get_all_people():
    items = list(coleccion.find())
    return items

# Operación para obtener una persona por ID
@app.get("/persona/{person_id}", response_model=PersonDto, tags=["Persona"])
def get_person_by_id(person_id: str):
    item = coleccion.find_one({"id": person_id})
    if item is not None:
        return item
    else:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

# Operación para obtener una persona por identificacion
@app.get("/persona/idenficacion/{person_identificacion}", response_model=PersonDto, tags=["Persona"])
def get_person_by_identification(person_identificacion: str):
    item = coleccion.find_one({"identification": person_identificacion})
    if item is not None:
        return item
    else:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    
# Operación para editar una persona por ID
@app.put("/persona/{person_id}", response_model=PersonDto, tags=["Persona"])
def update_person(person_id: int, updated_person: PersonDto):
    for index, person in enumerate(people_db):
        if person.id == person_id:
            people_db[index] = updated_person
            return updated_person
    raise HTTPException(status_code=404, detail="Persona no encontrada")

# Operación para eliminar una persona por ID
@app.delete("/persona/{person_id}", tags=["Persona"])
def delete_person(person_id: str):
    result = coleccion.delete_one({"id": person_id})
    if result.deleted_count == 1:
        return {"mensaje": "Persona eliminada correctamente"}
    else:
        raise HTTPException(status_code=404, detail="Persona no encontrada")