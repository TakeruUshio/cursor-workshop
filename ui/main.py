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


if __name__ == "__main__":
    main()
