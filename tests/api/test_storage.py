from api.storage import InMemoryStorage


def test_in_memory_storage_initialization() -> None:
    """InMemoryStorageクラスが正しく初期化されることをテストする"""
    storage = InMemoryStorage()
    assert storage._products == {}
    assert storage._next_id == 1
