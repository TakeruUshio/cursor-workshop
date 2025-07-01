import pytest
from pydantic import ValidationError

from api.models import ProductModel


def test_product_model_success() -> None:
    """商品モデルが正常なデータで作成できることをテストする"""
    data = {"id": 1, "name": "テスト商品", "price": 100.0}
    product = ProductModel(**data)
    assert product.id == data["id"]
    assert product.name == data["name"]
    assert product.price == data["price"]
    assert product.created_at is not None


def test_product_model_invalid_name() -> None:
    """商品名が空文字の場合にバリデーションエラーが発生することをテストする"""
    with pytest.raises(ValidationError):
        ProductModel(id=1, name="", price=100.0)


def test_product_model_invalid_price() -> None:
    """価格が0以下の場合にバリデーションエラーが発生することをテストする"""
    with pytest.raises(ValidationError):
        ProductModel(id=1, name="テスト商品", price=0)

    with pytest.raises(ValidationError):
        ProductModel(id=1, name="テスト商品", price=-100)
