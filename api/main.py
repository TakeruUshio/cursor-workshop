from fastapi import FastAPI

app = FastAPI(title="商品管理API")


@app.get("/health", summary="ヘルスチェック")
async def health_check() -> dict[str, str]:
    """APIの稼働状況を返すエンドポイント"""
    return {"status": "ok"}
