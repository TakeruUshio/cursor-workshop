from typing import List

from fastapi import FastAPI, HTTPException, status

from .models import ProductCreate, ProductModel
from .storage import InMemoryStorage

app = FastAPI(title="商品管理API")
storage = InMemoryStorage()


@app.on_event("startup")
async def startup_event() -> None:
    """アプリケーション起動時にストレージを初期化する"""
    storage.reset()


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


@app.get(
    "/items/{item_id}",
    response_model=ProductModel,
    status_code=status.HTTP_200_OK,
    summary="商品取得",
)
async def get_item(item_id: int) -> ProductModel:
    """IDで指定された商品を取得する"""
    product = storage.get_product(item_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product
