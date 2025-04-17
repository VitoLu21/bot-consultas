from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

consultas = []
CLAVE_SECRETA = "UNIVERSIDAD2025"

@app.middleware("http")
async def verificar_token(request: Request, call_next):
    # Si accede a /openapi.json, no requiere autorización
    if request.url.path == "/openapi.json":
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
    return FileResponse("openapi.json", media_type="application/json")
