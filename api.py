from fastapi import FastAPI, Header, HTTPException, Request
from datetime import datetime
import json
import os

app = FastAPI()

API_KEY = "secret123"
LOG_FILE = "loggedips.log"

# Create a fresh log file on every deployment/start
@app.on_event("startup")
def startup_event():
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("=== MINECRAFT IP LOGGER STARTED ===\n\n")

@app.get("/")
def home():
    return {
        "status": "API running",
        "logging": True,
        "endpoint": "/log"
    }

@app.get("/secure")
def secure(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"access": "granted"}

# ⭐ MAIN LOGGER ENDPOINT (your finder uses this)
@app.post("/log")
async def log_ip(request: Request, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    try:
        data = await request.json()
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    ip = data.get("ip", "unknown")
    info = data.get("info", {})

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = {
        "time": timestamp,
        "ip": ip,
        "players": info.get("players"),
        "max_players": info.get("max_players"),
        "version": info.get("version"),
        "source": info.get("source", "finder")
    }

    # Append to log file (auto created if missing)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

    return {
        "status": "logged",
        "ip": ip
    }
