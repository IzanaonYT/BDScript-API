from fastapi import APIRouter, HTTPException
import requests


router = APIRouter()




@router.get("/api/discord_users/")
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