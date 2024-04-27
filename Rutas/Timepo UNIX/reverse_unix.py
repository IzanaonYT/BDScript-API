from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import requests


router = APIRouter()





def convertir_tiempo(tiempo_unix):
    dias, segundos = divmod(tiempo_unix, 86400)
    horas, segundos = divmod(segundos, 3600)
    minutos, segundos = divmod(segundos, 60)
    
    resultado = ""
    
    if dias > 0:
        resultado += f"{dias} dia{'s' if dias > 1 else ''}"
        if horas > 0 or minutos > 0 or segundos > 0:
            resultado += " y "
    if horas > 0:
        resultado += f"{horas} hora{'s' if horas > 1 else ''}"
        if minutos > 0 or segundos > 0:
            resultado += " y "
    if minutos > 0:
        resultado += f"{minutos} minuto{'s' if minutos > 1 else ''}"
        if segundos > 0:
            resultado += " y "
    if segundos > 0:
        resultado += f"{segundos} segundo{'s' if segundos > 1 else ''}"
    
    return resultado.strip()


@router.get("/api/cooldown/")
async def convertir_tiempo_endpoint(unix: int):
    tiempo_legible = convertir_tiempo(unix)
    return {"tiempo_legible": tiempo_legible}
