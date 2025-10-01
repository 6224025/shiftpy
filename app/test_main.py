import pytest
from httpx import AsyncClient, ASGITransport

# FastAPIのアプリケーションインスタンスをインポート
from main import app 

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
    
    # ステータスコードが200であることを確認
    assert response.status_code == 200