from fastapi import FastAPI, Header, HTTPException, Request
from datetime import datetime

app = FastAPI()

API_KEY = "secret123"

# In-memory storage (Railway-safe)
LOG_STORAGE = []

@app.get("/")
def home():
    return {
        "status": "API running",
        "endpoints": {
            "post_log": "/log",
            "get_logs": "/logs"
        }
    }

# Finder sends data here
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

    entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": ip,
        "players": info.get("players"),
        "max_players": info.get("max_players"),
        "version": info.get("version"),
        "source": info.get("source", "finder")
    }

    LOG_STORAGE.append(entry)

    return {
        "status": "logged",
        "ip": ip,
        "stored_count": len(LOG_STORAGE)
    }

# Your external script will fetch logs from here
@app.get("/logs")
def get_logs(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    return {
        "count": len(LOG_STORAGE),
        "logs": LOG_STORAGE
    }

# Optional: clear logs endpoint
@app.delete("/logs")
def clear_logs(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    LOG_STORAGE.clear()
    return {"status": "cleared"}
