from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

consultas = []
CLAVE_SECRETA = "UNIVERSIDAD2025"

@app.middleware("http")
async def verificar_token(request: Request, call_next):
    token = request.headers.get("Authorization")
    if token != f"Bearer {CLAVE_SECRETA}":
        raise HTTPException(status_code=403, detail="No autorizado")
    return await call_next(request)

class Consulta(BaseModel):
    usuario: str
    mensaje: str

@app.post("/guardar_consulta")
async def guardar_consulta(data: Consulta):
    consultas.append({
        "usuario": data.usuario,
        "mensaje": data.mensaje,
        "fecha": datetime.now().isoformat()
    })
    return {"estado": "ok", "mensaje_guardado": data.mensaje}
from fastapi.responses import FileResponse

@app.get("/openapi.json")
async def serve_openapi():
    return FileResponse("openapi.json", media_type="application/json")
