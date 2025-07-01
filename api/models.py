from datetime import datetime

from pydantic import BaseModel, Field


class ProductModel(BaseModel):
    """商品データモデル"""

    id: int = Field(..., description="商品ID")
    name: str = Field(..., min_length=1, description="商品名")
    price: float = Field(..., gt=0, description="単価")
    created_at: datetime = Field(default_factory=datetime.now, description="作成日時")


class ProductCreate(BaseModel):
    """商品作成時に使用するデータモデル"""

    name: str = Field(..., min_length=1, description="商品名")
    price: float = Field(..., gt=0, description="単価")
