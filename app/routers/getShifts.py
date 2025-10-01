from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/api/getShifts", tags=["Shifts"])
async def get_shifts():
    # プロジェクトルートからの相対パスを取得
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, "sampledata.json")
    with open(json_path, "r") as f:
        data = f.read()
    return {"shifts": data}