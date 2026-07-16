from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.broadcasts import fetch_broadcasts
from app.config import settings

app = FastAPI(title="CV3 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/broadcasts")
async def get_broadcasts(type: str = Query("lb", pattern="^(lb|hs)$")):
    return await fetch_broadcasts(type)
