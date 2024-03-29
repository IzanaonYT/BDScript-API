from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response, JSONResponse, StreamingResponse
import json
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

app = FastAPI()




@app.get("/")
def on_route():
    variable = json.dumps({"API": "https://bdscript-api.onrender.com", "Extra": [{"HOST": "https://render.com", "Discord Soporte": "https://discord.gg/dru9uRYKqq"}], "Enpoints": ["/api/discord_users/?token=TOKEN&guild_id=ID_DE_SERVIDOR", "/api/invite_info/?token=TOKEN&guild_id=ID_DE_SERVIDOR&member_id=ID_DEL_MIEMBRO", "/api/roles_members/?token=TOKEN&guild_id=ID_DE_SERVIDOR [limit=NUMERO&page=NUMERO]", "/api/timestamp/?solicitud=TIEMPO",  "/api/get_bdfd/?code=CODE BDScript",
                                                                                                                                                                                   "/api/user_info/?token=TOKEN&guild_id=ID_SERVIDOR&user_id=ID_USUARIO"]}, indent=4)
    return Response(content=variable, media_type="application/json")

@app.get("/api/discord_users/")
def discord_users(token: str = None, guild_id: str = None):
    if token is None:
        raise HTTPException(status_code=404, detail="Error: Token no proporcionado")
    elif guild_id is None:
        raise HTTPException(status_code=400, detail="Error: ID de servidor no proporcionado")

    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v8/guilds/{guild_id}/members"
    response = requests.get(url, headers=headers, params={"limit": 1000})

    if response.status_code == 200:
        miembros = response.json()
        ids_miembros = [member['user']['id'] for member in miembros]
        return {"guild_id": guild_id, "members_ids": ids_miembros}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    

@app.get("/api/invite_info/")
def invite_info(token: str, guild_id: str, member_id: str):
    if token is None:
        raise HTTPException(status_code=404, detail="Error: Token no proporcionado")
    elif guild_id is None:
        raise HTTPException(status_code=400, detail="Error: ID de servidor no proporcionado")
    elif member_id is None:
        raise HTTPException(status_code=400, detail="Error: ID de miembro no proporcionado")
    headers = {
        "Authorization": f"Bot {token}"
    }

    response = requests.get(
        f"https://discord.com/api/v9/guilds/{guild_id}/members/{member_id}", headers=headers)

    if response.status_code == 200:
        member_data = response.json()
        if "joined_at" in member_data:
            joined_at = member_data["joined_at"]
            inviter_id = member_data["user"]["id"]

            invites_response = requests.get(
                f"https://discord.com/api/v9/guilds/{guild_id}/invites", headers=headers)
            if invites_response.status_code == 200:
                invites_data = invites_response.json()
                for invite in invites_data:
                    if invite["inviter"]["id"] == inviter_id:
                        return {
                            "invitation_code": invite["code"],
                            "inviter_id": inviter_id,
                            "joined_at": joined_at
                        }
    return JSONResponse(content={"error": "No se encontró información de la invitación", "status": 401}, status_code=401)






    
@app.get("/api/timestamp/")
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





@app.get("/api/roles_members/")
def miembros(token: str, guild_id: int, limit: int = 10, page: int = 1):
    headers = {
        'Authorization': f'Bot {token}',
        'Content-Type': 'application/json'
    }

    roles_response = requests.get(
        f'https://discord.com/api/v8/guilds/{guild_id}/roles', headers=headers)
    roles_data = roles_response.json()

    members_data = []
    after = 0
    while True:
        members_response = requests.get(
            f'https://discord.com/api/v8/guilds/{guild_id}/members?limit=1000&after={after}', headers=headers)
        batch = members_response.json()
        if not batch:
            break
        members_data.extend(batch)
        after = batch[-1]['user']['id']

    if roles_response.status_code == 200 and members_response.status_code == 200:
        roles_members = []
        for role in roles_data[(page - 1) * limit: page * limit]:
            role_id = role['id']
            role_name = role['name']

            member_count = sum(1 for member in members_data if role_id in [
                               r_id for r_id in member['roles']])
            roles_members.append(
                {"role_name": role_name, "role_count": member_count})

        return {
            "roles_members": roles_members,
            "total_pages": (len(roles_data) + limit - 1) // limit
        }
    else:
        if roles_response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Error al obtener roles: {roles_response.status_code}")
        if members_response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Error al obtener miembros: {members_response.status_code}")
        



@app.get("/api/user_info/")
def get_user_info(token: str=None, guild_id: int=None, user_id: int=None):
    if token is None:
        raise HTTPException(status_code=401, detail="Error: Token no proporcionado")
    elif guild_id is None:
        raise HTTPException(status_code=400, detail="Error: ID de servidor no proporcionado")
    elif user_id is None:
        raise HTTPException(status_code=400, detail="Error: ID de usuario no proporcionado")
    
    headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
    url = f"https://discord.com/api/guilds/{guild_id}/members/{user_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        retorno = response.json()
        return JSONResponse(content={"status": 200, "user_info": retorno}, status_code=200)
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    


def obtener_func(texto, funciones):
    obtenido = []
    for funcion in funciones:
        if funcion in texto:
            obtenido.append(funcion)
    return obtenido

@app.get("/api/get_bdfd/")
def get_bdfd(code: str):
    url = "https://botdesignerdiscord.com/public/api/function_tag_list"
    response = requests.get(url)
    funciones = response.json()
    obtener = obtener_func(code, funciones)
    if not len(obtener) == 0:
        return obtener



@app.get('/card')
async def generate_card(avatar: str = Query(...), middle: str = Query(...), name: str = Query(...),
                        bottom: str = Query(...), textcolor: str = '#FFFFFF', avatarborder: str = '#FFFFFF',
                        avatarbg: str = '#1F1F1F', background: str = ''):
    canvas = Image.new('RGB', (768, 375), 'white')
    ctx = ImageDraw.Draw(canvas)

    if background:
        if background.startswith('http'):
            try:
                response = requests.get(background)
                bg_image = Image.open(BytesIO(response.content))
                canvas.paste(bg_image, (0, 0))
            except:
                pass
        elif background.startswith('#') or background.startswith('rgba'):
            ctx.rectangle([(0, 0), (768, 375)], fill=background)

    font_50 = ImageFont.truetype('arial.ttf', 50)
    font_40 = ImageFont.truetype('arial.ttf', 40)
    font_30 = ImageFont.truetype('arial.ttf', 30)

    ctx.textsize(middle, font=font_50)
    ctx.text((384, 275), middle, fill=textcolor, font=font_50)

    ctx.textsize(name, font=font_40)
    ctx.text((384, 315), name, fill=textcolor, font=font_40)

    ctx.textsize(bottom, font=font_30)
    ctx.text((384, 350), bottom, fill=textcolor, font=font_30)

    if avatar:
        try:
            response = requests.get(avatar)
            avatar_image = Image.open(BytesIO(response.content))
            avatar_image = avatar_image.resize((210, 210))
            canvas.paste(avatar_image, (279, 25))
        except:
            pass

    img_io = BytesIO()
    canvas.save(img_io, 'PNG')
    img_io.seek(0)
    return StreamingResponse(img_io, media_type="image/png")
