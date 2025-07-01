import pytest
from httpx import ASGITransport, AsyncClient

from api.main import app  # 実装したのでコメントを外す


@pytest.mark.anyio
async def test_health_check() -> None:
    """GET /health が 200 OK と {"status": "ok"} を返すことをテストする"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    # assert False  # テストを実装したので削除
