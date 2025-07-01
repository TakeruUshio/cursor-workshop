import pytest
from httpx import ASGITransport, AsyncClient

from api.main import app, storage


@pytest.fixture(autouse=True)
def reset_storage() -> None:
    """各テストの前にストレージの状態をリセットする"""
    storage.__init__()


@pytest.mark.anyio
async def test_health_check() -> None:
    """GET /health が 200 OK と {"status": "ok"} を返すことをテストする"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    # assert False  # テストを実装したので削除


@pytest.mark.anyio
async def test_create_product_returns_201() -> None:
    """POST /items が正常なデータで 201 Created を返すことをテストする"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/items", json={"name": "テスト商品", "price": 1000})
    assert response.status_code == 201


@pytest.mark.anyio
async def test_create_product_returns_created_product() -> None:
    """POST /items が作成された商品データを返すことをテストする"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/items", json={"name": "テスト商品", "price": 1000})

    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "テスト商品"
    assert data["price"] == 1000
    assert "created_at" in data


@pytest.mark.parametrize(
    ("payload", "error_message"),
    [
        ({"name": "", "price": 1000}, "String should have at least 1 character"),
        ({"name": "テスト商品", "price": 0}, "Input should be greater than 0"),
        ({"name": "テスト商品", "price": -1}, "Input should be greater than 0"),
    ],
)
@pytest.mark.anyio
async def test_create_product_with_invalid_data_returns_422(
    payload: dict, error_message: str
) -> None:
    """不正なデータで商品を作成しようとすると 422 エラーが返ることをテストする"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/items", json=payload)

    assert response.status_code == 422
    assert error_message in response.text
