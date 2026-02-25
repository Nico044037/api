from fastapi import FastAPI, Header, HTTPException

app = FastAPI()
API_KEY = "secret123"

@app.get("/")
def home():
    return {"status": "API running"}

@app.get("/secure")
def secure(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"access": "granted"}
