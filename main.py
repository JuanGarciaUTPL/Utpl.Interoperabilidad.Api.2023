from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

#libreria para generar un id unico
import uuid

#importar librerias para el manejo de la base de datos pymongo
import pymongo

#libreria para el manejo de versiones
#from versioned_fastapi import version, FastApiVersioner

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
    email: str
    identification: str
    city: str
    status: Optional[str]



# Modelo de datos para una persona v2
class PersonDtoV2(BaseModel):
    name: str
    age: int
    email: str
    identification: str
    city: str
    marital_status: str
        

# Modelo de datos para una persona con ID, para conectar con la base de datos
class PersonRepository(BaseModel):
    name: str
    age: int
    email: str
    identification: str
    city: str
    id: str
    marital_status: Optional[str]

# Lista para almacenar personas (simulación de base de datos)
people_db = []

# Operación para crear una persona
#@version(1)
@app.post("/persona/", response_model=PersonRepository, tags=["Persona"])
def create_person(personInput: PersonDto):
    idPerson = str(uuid.uuid4())
    itemPersona = PersonRepository(name=personInput.name, age=personInput.age, email=personInput.email, identification=personInput.identification, city=personInput.city, id=idPerson)
    result = coleccion.insert_one(itemPersona.dict())
    return itemPersona

# Operación para crear una persona v2
#@version(2)
@app.post("/persona/", response_model=PersonRepository, tags=["Persona"])
def create_person(personInput: PersonDtoV2):
    idPerson = str(uuid.uuid4())
    itemPersona = PersonRepository(name=personInput.name, age=personInput.age, email=personInput.email, identification=personInput.identification, city=personInput.city, id=idPerson, marital_status=personInput.marital_status)
    result = coleccion.insert_one(itemPersona.dict())
    return itemPersona

# Operación para obtener todas las personas
#@version(1)
@app.get("/persona/", response_model=List[PersonRepository], tags=["Persona"])
def get_all_people():
    items = list(coleccion.find())
    return items

# Operación para obtener una persona por ID
#@version(1)
@app.get("/persona/{person_id}", response_model=PersonDto, tags=["Persona"])
def get_person_by_id(person_id: str):
    item = coleccion.find_one({"id": person_id})
    if item is not None:
        return item
    else:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

# Operación para obtener una persona por identificacion
#@version(1)
@app.get("/persona/idenficacion/{person_identificacion}", response_model=PersonDto, tags=["Persona"])
def get_person_by_identification(person_identificacion: str):
    item = coleccion.find_one({"identification": person_identificacion})
    if item is not None:
        return item
    else:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    
# Operación para editar una persona por ID
#@version(1)
@app.put("/persona/{person_id}", tags=["Persona"])
def update_person(person_id: str, updated_person: PersonDto):
    item = coleccion.find_one({"id": person_id})
    if item is not None:
        updated_person = { "$set": { "name": updated_person.name, "age": updated_person.age, "email": updated_person.email, "identification": updated_person.identification, "city": updated_person.city } }
        coleccion.update_one(item, updated_person)
        return {"mensaje": "Persona actualizada correctamente"}
    else:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

# Operación para eliminar una persona por ID
#@version(1)
@app.delete("/persona/{person_id}", tags=["Persona"])
def delete_person(person_id: str):
    result = coleccion.delete_one({"id": person_id})
    if result.deleted_count == 1:
        return {"mensaje": "Persona eliminada correctamente"}
    else:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

# Version your app
# It will add version prefixes and customize the swagger docs
#versions = FastApiVersioner(app).version_fastapi()