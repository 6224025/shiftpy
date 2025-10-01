from fastapi import APIRouter
from ..config import settings


router = APIRouter()

@router.post("/api/login", tags=["Authentication"])
async def login():
    # ここにログイン処理を記述
    return {"status": "login successful"}