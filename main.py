from fastapi import FastAPI, HTTPException
from fastapi.responses import Response, JSONResponse
import json
import requests
app = FastAPI()




@app.get("/")
def on_route():
    variable = json.dumps({"API": "https://{localhost}/api/endpoints.json", "Extra": [{"HOST": "https://render.com", "Discord Soporte": "https://discord.gg/dru9uRYKqq"}]}, indent=4)
    return Response(content=variable, media_type="application/json")

@app.get("/api/discord_users/.json")
def discord_users(token: str = None, guild_id: str = None):
    if token is None:
        raise HTTPException(status_code=404, detail="Error: Token no proporcionado")
    elif guild_id is None:
        raise HTTPException(status_code=400, detail="Error: ID de servidor no proporcionado")

    headers = {"Authorization": f"Bearer {token}"}

    url = f"https://discord.com/api/v8/guilds/{guild_id}/members"
    response = requests.get(url, headers=headers, params={"limit": 100})

    if response.status_code == 200:
        miembros = response.json()
        var = {"guild_id": guild_id, "members_ids": []}
        for member in miembros:
            var["members_ids"].append(member['user']['id'])
        return var
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
