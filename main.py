from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import re, os

app = FastAPI()

class SlugRequest(BaseModel):
    title: str

BACKEND_SECRET = os.getenv("BACKEND_SECRET")

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text

@app.middleware("http")
async def verify_backend_secret(request: Request, call_next):
    if BACKEND_SECRET:  # Only check if set
        header_secret = request.headers.get("x-backend-secret")
        if header_secret != BACKEND_SECRET:
            raise HTTPException(status_code=401, detail="Unauthorized")
    return await call_next(request)

@app.post("/v1/slugify")
async def create_slug(req: SlugRequest):
    return {"slug": slugify(req.title)}
