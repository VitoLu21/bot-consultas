from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
import json
import os

app = FastAPI()

CLAVE_SECRETA = "UNIVERSIDAD2025"
ARCHIVO_JSON = "consultas.json"

# Cargar consultas previas si existe el archivo
if os.path.exists(ARCHIVO_JSON):
    with open(ARCHIVO_JSON, "r") as f:
        consultas = json.load(f)
else:
    consultas = []

class Consulta(BaseModel):
    usuario: str
    mensaje: str

@app.middleware("http")
async def verificar_token(request: Request, call_next):
    if request.url.path in ["/openapi.json", "/favicon.ico"]:
        return await call_next(request)

    token = request.headers.get("Authorization")
    if token != f"Bearer {CLAVE_SECRETA}":
        raise HTTPException(status_code=403, detail="No autorizado")

    return await call_next(request)

@app.post("/guardar_consulta")
async def guardar_consulta(data: Consulta):
    nueva_consulta = {
        "usuario": data.usuario,
        "mensaje": data.mensaje,
        "fecha": datetime.now().isoformat()
    }

    consultas.append(nueva_consulta)

    # Guardar en el archivo JSON
    with open(ARCHIVO_JSON, "w") as f:
        json.dump(consultas, f, indent=4)

    return {"estado": "ok", "mensaje_guardado": data.mensaje}

@app.get("/ver_consultas")
def ver_consultas():
    return JSONResponse(content=consultas)

@app.get("/openapi.json")
async def serve_openapi():
    with open("openapi.json") as f:
        data = json.load(f)
    return JSONResponse(content=data)
