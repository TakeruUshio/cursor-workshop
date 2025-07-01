import httpx
import streamlit as st
from pydantic import BaseModel, Field

API_URL = "http://localhost:8000"


class ProductCreate(BaseModel):
    """商品作成リクエストモデル"""

    name: str = Field(..., min_length=1, description="商品名")
    price: float = Field(..., gt=0, description="単価")


def main() -> None:
    """メイン関数"""
    st.title("かんたん商品管理")

    # --- 商品登録フォーム ---
    st.subheader("商品を登録する")
    product_name = st.text_input("商品名", key="product_name")
    product_price = st.number_input("価格", min_value=1, key="product_price")
    if st.button("商品を登録する", key="create_product"):
        if not product_name:
            st.error("商品名を入力してください。")
        else:
            try:
                product_data = ProductCreate(name=product_name, price=product_price)
                response = httpx.post(f"{API_URL}/items", json=product_data.model_dump())

                if response.status_code == 201:
                    new_product = response.json()
                    st.session_state.products.append(new_product)
                    st.success(f"商品「{new_product['name']}」を登録しました。")
                else:
                    st.error(f"エラー: {response.status_code} - {response.text}")
            except httpx.RequestError as e:
                st.error(f"APIへの接続に失敗しました: {e}")
            except Exception as e:
                st.error(f"予期せぬエラーが発生しました: {e}")

    # --- 登録済み商品一覧 ---
    st.subheader("登録済み商品一覧")

    # セッション状態に商品リストがなければ初期化
    if "products" not in st.session_state:
        st.session_state.products = []

    # 商品一覧表示
    if not st.session_state.products:
        st.info("まだ商品が登録されていません。")
    else:
        for product in st.session_state.products:
            with st.container():
                st.write(f"ID: {product.get('id', 'N/A')}")
                st.write(f"商品名: {product.get('name', 'N/A')}")
                st.write(f"価格: {product.get('price', 'N/A')} 円")
                st.write(f"登録日時: {product.get('created_at', 'N/A')}")


if __name__ == "__main__":
    main()
