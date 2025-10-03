"""Routers for updating shift data."""

from __future__ import annotations

from pathlib import Path
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator

router = APIRouter()


DATA_FILE: Path = Path(__file__).resolve().parents[2] / "sample.json"


class Shift(BaseModel):
    name: str
    StudentId: str
    jobName: str
    shiftDate: str
    startTime: str
    endTime: str

    @field_validator("startTime", "endTime")
    @classmethod
    def validate_time_format(cls, value: str) -> str:
        if len(value) != 5 or value[2] != ":":
            raise ValueError("Time must be in HH:MM format")
        hour, minute = value.split(":", 1)
        if not hour.isdigit() or not minute.isdigit():
            raise ValueError("Time must contain digits")
        hour_int = int(hour)
        minute_int = int(minute)
        if not (0 <= hour_int <= 23 and 0 <= minute_int <= 59):
            raise ValueError("Time must represent a valid 24-hour clock value")
        return value


class ShiftCollection(BaseModel):
    shifts: List[Shift] = Field(default_factory=list)


INITIAL_SAMPLE_STATE_DICT = {
    "shifts": [
        {
            "name": "Lagrange",
            "StudentId": "S001",
            "jobName": "Cashier",
            "shiftDate": "2024-07-01",
            "startTime": "09:00",
            "endTime": "13:00",
        }
    ]
}

INITIAL_SAMPLE_STATE = ShiftCollection.model_validate(INITIAL_SAMPLE_STATE_DICT)


def _save_shift_data(file_path: Path, data: dict) -> None:
    import json

    file_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True),
        encoding="utf-8",
    )


@router.post("/api/updateShift", tags=["Shifts"])
async def update_shift(payload: ShiftCollection):
    """Replace shift dataset with provided payload after resetting to baseline."""

    # Reset sample.json to baseline for verification
    _save_shift_data(DATA_FILE, INITIAL_SAMPLE_STATE.model_dump())

    # Apply incoming request data to sample.json
    result = payload.model_dump()
    _save_shift_data(DATA_FILE, result)

    return {
        "status": "shift data applied successfully",
        "count": len(payload.shifts),
        "shifts": result["shifts"],
    }