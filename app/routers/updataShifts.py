from fastapi import APIRouter

router = APIRouter()

@router.post("/api/updateShift", tags=["Shifts"])
async def update_shift():
    # ここにシフト情報を更新する処理を記述
    return {"status": "shift updated"}