from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import requests

router = APIRouter()



@router.get("/api/invite_info/")
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
