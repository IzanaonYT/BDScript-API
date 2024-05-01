from fastapi import FastAPI, HTTPException, Query,APIRouter
from fastapi.responses import Response, JSONResponse, StreamingResponse
import json
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from pydantic import BaseModel
import os
import importlib.util
app = FastAPI()



def registrar_rutas_desde_directorio(router, directorio):
    for nombre_archivo in os.listdir(directorio):
        ruta_completa = os.path.join(directorio, nombre_archivo)
        if os.path.isdir(ruta_completa):
            registrar_rutas_desde_directorio(router, ruta_completa)
        elif nombre_archivo.endswith('.py') and nombre_archivo != '__init__.py':
            nombre_modulo = nombre_archivo[:-3]
            spec = importlib.util.spec_from_file_location(f"API.{nombre_modulo}", ruta_completa)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            if hasattr(modulo, 'router'):
                router.include_router(modulo.router)

carpeta_api = os.path.join(os.path.dirname(__file__), 'Rutas')
router_principal = APIRouter()

registrar_rutas_desde_directorio(router_principal, carpeta_api)
app.include_router(router_principal)


@app.get("/")
def on_route():
    variable = json.dumps({"API": "https://bdscript-api.onrender.com", 
                           "Extra": [{"HOST": "https://render.com", "Discord Soporte": "https://discord.gg/dru9uRYKqq"}], 
                           "Enpoints": ["/api/discord_users/?token=TOKEN&guild_id=ID_DE_SERVIDOR", 
                                        "/api/invite_info/?token=TOKEN&guild_id=ID_DE_SERVIDOR&member_id=ID_DEL_MIEMBRO", 
                                        "/api/roles_members/?token=TOKEN&guild_id=ID_DE_SERVIDOR [limit=NUMERO&page=NUMERO]", 
                                        "/api/timestamp/?solicitud=TIEMPO",  
                                        "/api/get_bdfd/?code=CODE BDScript",
                                        "/api//api/emojis_get/?guild_id=ID_SERVIDOR + HEADERNAME: token, VALUE: TOKENBOT"
                                                                                                                                                                                   "/api/user_info/?token=TOKEN&guild_id=ID_SERVIDOR&user_id=ID_USUARIO"]}, indent=4)
    return Response(content=variable, media_type="application/json")


    








    














