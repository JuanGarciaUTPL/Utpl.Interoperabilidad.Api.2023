from fastapi import FastAPI, HTTPException

app = FastAPI()

# Datos de ejemplo para personas
personas = [
    {"id": 1, "nombre": "Juan", "edad": 30},
    {"id": 2, "nombre": "María", "edad": 25},
    {"id": 3, "nombre": "Pedro", "edad": 35},
    {"id": 4, "nombre": "Felpe", "edad": 36},
]

# Ruta para listar todas las personas
@app.get("/personas")
async def listar_personas():
    return personas

# Ruta para obtener una persona por ID
@app.get("/personas/{persona_id}")
async def obtener_persona(persona_id: int):
    persona = next((p for p in personas if p["id"] == persona_id), None)
    if persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

# Ruta para eliminar una persona por ID
@app.delete("/personas/{persona_id}")
async def eliminar_persona(persona_id: int):
    persona = next((p for p in personas if p["id"] == persona_id), None)
    if persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    personas.remove(persona)
    return {"message": "Persona eliminada"}

# Ruta para actualizar una persona por ID
@app.put("/personas/{persona_id}")
async def actualizar_persona(persona_id: int, nueva_informacion: dict):
    persona = next((p for p in personas if p["id"] == persona_id), None)
    if persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    persona.update(nueva_informacion)
    return {"message": "Persona actualizada", "nueva_informacion": nueva_informacion}
