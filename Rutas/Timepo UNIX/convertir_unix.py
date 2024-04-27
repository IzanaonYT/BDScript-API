from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import requests


router = APIRouter()



@router.get("/api/timestamp/")
def convertir_a_segundos(solicitud):
    unidades = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'y': 31536000}
    resultado = 0
    cantidad = ''
    for caracter in solicitud:
        if caracter.isdigit():
            cantidad += caracter
        elif caracter in unidades:
            resultado += int(cantidad) * unidades[caracter]
            cantidad = ''
    if resultado == 0 :
        n = 404
    else:
        n = 200
    expos = {"result": resultado, "code": n}
    return JSONResponse(content=expos, status_code=200)