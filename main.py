# main.py
import os
import re
import unicodedata
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Slugify API (Demo)")

# Load allowed API keys from env (comma-separated) or default demo key
def load_allowed_keys():
    env = os.getenv("ALLOWED_KEYS")
    if env:
        return {k.strip(): "env" for k in env.split(",") if k.strip()}
    return {"demo-key-123": "demo"}

ALLOWED_KEYS = load_allowed_keys()
DISABLE_AUTH = os.getenv("DISABLE_AUTH", "0") == "1"

def check_api_key(x_api_key: Optional[str]):
    if DISABLE_AUTH:
        return
    if not x_api_key or x_api_key not in ALLOWED_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")

class SlugIn(BaseModel):
    title: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/slugify")
def slugify(payload: SlugIn, x_api_key: Optional[str] = Header(None)):
    """
    Example input:
    { "title": "Hello World: My First API!!" }
    """
    check_api_key(x_api_key)
    s = unicodedata.normalize("NFKD", payload.title)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    slug = re.sub(r"[-\s]+", "-", s)
    return {"slug": slug}
