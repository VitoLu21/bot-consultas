from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
import json
import os

app = FastAPI()

consultas = []
CLAVE_SECRETA = "UNIVERSIDAD2025"

class Consulta(BaseModel):
    usuario: str
    mensaje: str

@app.middleware("http")
async def verificar_token(request: Request, call_next):
    # Excluir rutas públicas del control de autorización
    if request.url.path in ["/openapi.json", "/favicon.ico"]:
        return await call_next(request)

    token = request.headers.get("Authorization")
    if token != f"Bearer {CLAVE_SECRETA}":
        raise HTTPException(status_code=403, detail="No autorizado")

    return await call_next(request)



@app.post("/guardar_consulta")
async def guardar_consulta(data: Consulta):
    consultas.append({
        "usuario": data.usuario,
        "mensaje": data.mensaje,
        "fecha": datetime.now().isoformat()
    })
    return {"estado": "ok", "mensaje_guardado": data.mensaje}


@app.get("/openapi.json")
async def serve_openapi():
    with open("openapi.json") as f:
        data = json.load(f)
    return JSONResponse(content=data)
