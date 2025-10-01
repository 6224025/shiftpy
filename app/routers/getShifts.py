from fastapi import APIRouter
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

@router.get(os.getenv("api/getShifts"), tags=["Shifts"])
async def get_shifts():
    with open("sampledata.json", "r") as f:
        data = f.read()
    return {"shifts": data}