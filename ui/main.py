import streamlit as st


def main() -> None:
    """メイン関数"""
    st.title("かんたん商品管理")

    # --- 商品登録フォーム ---
    st.subheader("商品を登録する")
    product_name = st.text_input("商品名", key="product_name")  # noqa: F841
    product_price = st.number_input("価格", min_value=1, key="product_price")  # noqa: F841
    st.button("商品を登録する", key="create_product")

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
