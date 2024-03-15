from fastapi import FastAPI, HTTPException
from fastapi.responses import Response, JSONResponse
import json
import requests
app = FastAPI()




@app.get("/")
def on_route():
    variable = json.dumps({"API": "https://bdscript-api.onrender.com", "Extra": [{"HOST": "https://render.com", "Discord Soporte": "https://discord.gg/dru9uRYKqq"}], "Enpoints": ["/api/discord_users/?token=TOKEN&guild_id=ID_DE_SERVIDOR", "/api/invite_info/?token=TOKEN&guild_id=ID_DE_SERVIDOR&member_id=ID_DEL_MIEMBRO", "/api/roles_members/?token=TOKEN&guild_id=ID_DE_SERVIDOR [limit=NUMERO&page=NUMERO]", "/api/timestamp/?solicitud=TIEMPO"]}, indent=4)
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
def get_user_info(token: str=None, guild_id: str=None, user_id: str=NotImplemented):
    if token is None:
        raise HTTPException(status_code=404, detail="Error: Token no proporcionado")
    elif guild_id is None:
        raise HTTPException(status_code=400, detail="Error: ID de servidor no proporcionado")
    elif user_id is None:
        raise HTTPException(status_code=400, detail="Error: ID de usuario no proporcionado")
    
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    response = requests.get(f"https://discord.com/api/guilds/{guild_id}/members/{user_id}", headers=headers)
    if response.status_code == 200:
        retorno = response.json()
        return JSONResponse(content={"status": 200, "use_info": [retorno]}, status_code=200)