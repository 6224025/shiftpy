from fastapi import APIRouter

# APIRouterのインスタンスを作成
router = APIRouter()

@router.post("/api/login", tags=["Authentication"])
async def login():
    # ここにログイン処理を記述
    return {"status": "login successful"}