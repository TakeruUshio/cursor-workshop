import re

from playwright.sync_api import Page, expect


def test_product_creation_journey(page: Page) -> None:
    """ユーザーがUIを通じて商品を登録する一連の流れをテストするE2Eテスト。"""
    # ステップ1: Streamlitアプリのページを開く
    page.goto("http://localhost:8501/")

    # ページのタイトルに "Streamlit" が含まれていることを確認
    expect(page).to_have_title(re.compile("Streamlit"))

    # ステップ2: 商品名と価格を入力する
    page.get_by_label("商品名").fill("テスト商品")
    page.get_by_label("価格").fill("999")

    # ステップ3: 「商品を登録する」ボタンをクリックする
    # Streamlitのボタンはしばしば複数の要素を含むため、より確実にテキストでボタンを特定する
    page.get_by_role("button", name=re.compile("商品を登録する")).click()

    # ステップ4: 登録成功メッセージが表示されることを確認する
    # `st.success` は `[data-testid="stAlert"]` というdiv要素としてレンダリングされる
    success_message = page.locator(
        '[data-testid="stAlert"]', has_text=re.compile("商品「テスト商品」を登録しました。")
    )
    expect(success_message).to_be_visible(timeout=10000)

    # ステップ5: 登録した商品が一覧に表示されることを確認する
    # 一覧表示エリアを特定し、その中に期待する情報が含まれているか検証する
    product_list_locator = page.get_by_text("登録済み商品一覧")
    product_list = page.locator('[data-testid="stVerticalBlock"]', has=product_list_locator)

    expect(product_list.get_by_text("ID: 1")).to_be_visible()
    expect(product_list.get_by_text("商品名: テスト商品")).to_be_visible()
    expect(product_list.get_by_text("価格: 999.0 円")).to_be_visible()
