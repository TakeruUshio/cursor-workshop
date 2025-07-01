from .models import ProductModel


class InMemoryStorage:
    """インメモリで商品データを管理するストレージクラス"""

    def __init__(self) -> None:
        self._products: dict[int, ProductModel] = {}
        self._next_id: int = 1

    def create_product(self, product_data: dict) -> ProductModel:
        """商品を新規作成する (Task #4で実装)"""
        raise NotImplementedError

    def get_product(self, product_id: int) -> ProductModel | None:
        """商品IDを指定して商品を取得する (Task #5で実装)"""
        raise NotImplementedError
