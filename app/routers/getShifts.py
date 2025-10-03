from typing import Optional

import json
from pathlib import Path

from fastapi import APIRouter

router = APIRouter()


DATA_FILE: Path = Path(__file__).resolve().parents[2] / "sample.json"


def _load_shifts(file_path: Path) -> dict:
    if not file_path.exists():
        return {"shifts": []}

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/api/getShifts", tags=["Shifts"])
async def get_shifts(studentId: Optional[str] = None):
    data = _load_shifts(DATA_FILE)

    shifts = data.get("shifts", [])

    if studentId:
        student_id_str = str(studentId)
        shifts = [shift for shift in shifts if str(shift.get("StudentId")) == student_id_str]

    return {"shifts": shifts}