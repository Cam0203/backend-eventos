from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from correo_service import enviar_correo

router = APIRouter(prefix="/correo", tags=["Correo"])

class CorreoRequest(BaseModel):
    destinatario: EmailStr
    asunto: str
    mensaje: str

@router.post("/enviar")
async def enviar(data: CorreoRequest):
    try:
        await enviar_correo(data.destinatario, data.asunto, data.mensaje)
        return {"mensaje": "Correo enviado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))