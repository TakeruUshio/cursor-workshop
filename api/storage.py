from .models import ProductCreate, ProductModel


class InMemoryStorage:
    """インメモリで商品データを管理するストレージクラス"""

    def __init__(self) -> None:
        self._products: dict[int, ProductModel] = {}
        self._next_id: int = 1

    def create_product(self, product_create: ProductCreate) -> ProductModel:
        """商品を新規作成する"""
        product_id = self._next_id
        product = ProductModel(id=product_id, **product_create.model_dump())
        self._products[product_id] = product
        self._next_id += 1
        return product

    def get_product(self, product_id: int) -> ProductModel | None:
        """商品IDを指定して商品を取得する"""
        return self._products.get(product_id)
