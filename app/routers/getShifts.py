from typing import Optional

import json
import os

from fastapi import APIRouter

router = APIRouter()

@router.get("/api/getShifts", tags=["Shifts"])
async def get_shifts(studentId: Optional[str] = None):

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, "sampledata.json")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    shifts = data.get("shifts", [])

    if studentId:
        student_id_str = str(studentId)
        shifts = [shift for shift in shifts if str(shift.get("StudentId")) == student_id_str]

    return {"shifts": shifts}