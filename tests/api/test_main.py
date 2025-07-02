import pytest
from httpx import ASGITransport, AsyncClient

from api.main import create_app


@pytest.fixture
async def async_client() -> AsyncClient:
    """各テストで独立したアプリケーションインスタンスと非同期クライアントを生成する"""
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.mark.anyio
async def test_health_check(async_client: AsyncClient) -> None:
    """GET /health が 200 OK と {"status": "ok"} を返すことをテストする"""
    response = await async_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_create_product_returns_201(async_client: AsyncClient) -> None:
    """POST /items が正常なデータで 201 Created を返すことをテストする"""
    response = await async_client.post("/items", json={"name": "テスト商品", "price": 1000})
    assert response.status_code == 201


@pytest.mark.anyio
async def test_create_product_returns_created_product(async_client: AsyncClient) -> None:
    """POST /items が作成された商品データを返すことをテストする"""
    response = await async_client.post("/items", json={"name": "テスト商品", "price": 1000})

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
    async_client: AsyncClient, payload: dict, error_message: str
) -> None:
    """不正なデータで商品を作成しようとすると 422 エラーが返ることをテストする"""
    response = await async_client.post("/items", json=payload)

    assert response.status_code == 422
    assert error_message in response.text


@pytest.mark.anyio
async def test_get_product_with_existing_id_returns_200(async_client: AsyncClient) -> None:
    """GET /items/{id} が存在するIDの場合に 200 OK と商品データを返すことをテストする"""
    # まず商品を作成
    create_response = await async_client.post("/items", json={"name": "テスト商品", "price": 1000})
    assert create_response.status_code == 201
    created_product_id = create_response.json()["id"]

    # 作成した商品をIDで取得
    get_response = await async_client.get(f"/items/{created_product_id}")

    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == created_product_id
    assert data["name"] == "テスト商品"
    assert data["price"] == 1000


@pytest.mark.anyio
async def test_get_product_with_non_existing_id_returns_404(async_client: AsyncClient) -> None:
    """GET /items/{id} が存在しないIDの場合に 404 Not Found を返すことをテストする"""
    response = await async_client.get("/items/999")  # 存在しないID

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}
