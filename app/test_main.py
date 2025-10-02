import pytest
from httpx import ASGITransport, AsyncClient

# FastAPIのアプリケーションインスタンスをインポート
from app.main import app

# pytestで非同期テストを実行するための設定
@pytest.mark.asyncio
async def test_get_shifts():
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
async def test_get_shifts_filtered_by_student_id():
    """studentIdクエリで対象のシフトのみ取得できるかテストする"""
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/getShifts", params={"studentId": "S001"})

    assert response.status_code == 200

    data = response.json()
    assert data.get("shifts")
    assert all(shift.get("StudentId") == "S001" for shift in data["shifts"])
    assert len(data["shifts"]) == 1