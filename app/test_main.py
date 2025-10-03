import json
import shutil
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

# FastAPIのアプリケーションインスタンスをインポート
from app.main import app
from app.routers import getShifts, updataShifts


@pytest.fixture()
def isolated_shift_data(tmp_path, monkeypatch):
    """Provide a temporary copy of shift data for tests that mutate it."""
    temp_file = tmp_path / "sample.json"
    original_path = Path(updataShifts.DATA_FILE)
    shutil.copy(original_path, temp_file)

    monkeypatch.setattr(updataShifts, "DATA_FILE", temp_file)
    monkeypatch.setattr(getShifts, "DATA_FILE", temp_file)

    yield temp_file

# pytestで非同期テストを実行するための設定
@pytest.mark.asyncio
async def test_get_shifts(isolated_shift_data):
    """
    /api/getShifts エンドポイントが正常に動作するかテストする
    """
    # appをASGITransportでラップする
    transport = ASGITransport(app=app)
    
    # AsyncClientには transport 引数として渡す
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/getShifts")

    assert response.status_code == 200

    data = response.json()
    assert "shifts" in data
    assert len(data["shifts"]) > 0


@pytest.mark.asyncio
async def test_get_shifts_filtered_by_student_id(isolated_shift_data):
    """studentIdクエリで対象のシフトのみ取得できるかテストする"""
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/getShifts", params={"studentId": "S001"})

    assert response.status_code == 200

    data = response.json()
    assert data.get("shifts")
    assert all(shift.get("StudentId") == "S001" for shift in data["shifts"])
    assert len(data["shifts"]) >= 1


@pytest.mark.asyncio
async def test_update_shift_replaces_dataset(isolated_shift_data):
    """POSTしたシフト一覧でsample.jsonが置き換わる"""
    transport = ASGITransport(app=app)
    payload = {
        "shifts": [
            {
                "name": "Alice",
                "StudentId": "S001",
                "jobName": "Cashier",
                "shiftDate": "2024-07-01",
                "startTime": "09:00",
                "endTime": "13:00",
            },
            {
                "name": "Bob",
                "StudentId": "S002",
                "jobName": "Chef",
                "shiftDate": "2024-07-01",
                "startTime": "10:00",
                "endTime": "18:00",
            },
        ]
    }

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/updateShift", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "shift data applied successfully"
    assert data["count"] == 2

    stored = json.loads(isolated_shift_data.read_text(encoding="utf-8"))
    assert stored == payload


@pytest.mark.asyncio
async def test_update_shift_allows_empty_payload(isolated_shift_data):
    """空のシフト一覧でもエラーにならず置き換えできる"""
    transport = ASGITransport(app=app)
    payload = {"shifts": []}

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/updateShift", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0

    stored = json.loads(isolated_shift_data.read_text(encoding="utf-8"))
    assert stored == payload