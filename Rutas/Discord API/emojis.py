from fastapi import APIRouter, Header, Query
import requests

router = APIRouter()

def obtener_emoji_paginado(token: str, guild_id: str, page: int, pageult: bool = False):
    url = f"https://discord.com/api/v9/guilds/{guild_id}/emojis"
    headers = {
        "Authorization": f"Bot {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        emojis = response.json()
        total_pages = len(emojis)
        
        if pageult:
            page = total_pages - 1
        
        if 0 <= page < total_pages:
            emoji_id = emojis[page]["id"]
            emoji_url = f"https://discord.com/api/v9/guilds/{guild_id}/emojis/{emoji_id}"
            emoji_response = requests.get(emoji_url, headers=headers)
            if emoji_response.status_code == 200:
                emoji_info = emoji_response.json()
                emoji_type = "Animado" if emoji_info.get("animated") else "Emoji Normal"
                emoji_info["type"] = emoji_type
                return {"emoji": emoji_info, "pagina": page + 1, "pages_total": total_pages}
        
        return []
    else:
        return None

@router.get("/api/emojis_get/{guild_id}/")
def get(guild_id: str, page: int = Query(0, ge=0), pageult: bool = Query(False), token: str = Header(None)):
    if token is None:
        return {"error": "Se requiere el token del bot en el encabezado"}
    
    emoji_paginado = obtener_emoji_paginado(token, guild_id, page, pageult)
    if emoji_paginado is not None:
        return emoji_paginado
    else:
        return {"error": "Error al obtener emoji del servidor"}




