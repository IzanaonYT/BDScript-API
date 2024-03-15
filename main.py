from fastapi import FastAPI, HTTPException
from fastapi.responses import Response, JSONResponse
import json
app = FastAPI()




@app.get("/")
def on_route():
    variable = json.dumps({"API": "https://{localhost}/api/endpoints.json", "Extra": [{"HOST": "https://render.com", "Discord Soporte": "https://discord.gg/dru9uRYKqq"}]}, indent=4)
    return Response(content=variable, media_type="application/json")
