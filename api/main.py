from fastapi import FastAPI
from starlette import status

from .models import ProductCreate, ProductModel
from .storage import InMemoryStorage

app = FastAPI(title="商品管理API")
storage = InMemoryStorage()


@app.get("/health", summary="ヘルスチェック", status_code=status.HTTP_200_OK)
async def health_check() -> dict[str, str]:
    """APIの稼働状況を返すエンドポイント"""
    return {"status": "ok"}


@app.post(
    "/items",
    response_model=ProductModel,
    status_code=status.HTTP_201_CREATED,
    summary="商品作成",
)
async def create_item(item: ProductCreate) -> ProductModel:
    """新しい商品を作成する"""
    return storage.create_product(item)
