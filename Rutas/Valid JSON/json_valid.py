from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, Response
import requests
import json

router = APIRouter()


@router.get("/api/valid_json/")
def validar_json(body):
    try:
        owo = json.loads(body)
        n = owo
    except ValueError:
        n = False

    if not n:
        pop = json.dumps({"status": 404, "detail": "JSON no valido"}, indent=4)
        return Response(content=pop, status_code=404, media_type="application/json")
    else:
        
        return Response(content=json.dumps(n, indent=4), status_code=200, media_type="application/json")
    

