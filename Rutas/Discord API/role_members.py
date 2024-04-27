from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()





@router.get("/api/roles_members/")
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
        