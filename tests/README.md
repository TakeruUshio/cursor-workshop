# テストの実行方法

このドキュメントでは、本プロジェクトに含まれる各種テストの実行方法について説明します。

## 1. 全ての単体・統合テストの実行

API の単体テストや統合テストなど、Playwright を使用しない全てのテストを一度に実行します。

```bash
uv run pytest
```

## 2. 個別テストの実行

特定のテストファイルのみを実行する場合は、ファイルパスを指定します。

```bash
# APIのメインロジックに関するテストのみ実行
uv run pytest tests/api/test_main.py

# モデルに関するテストのみ実行
uv run pytest tests/api/test_models.py
```

## 3. E2E（エンドツーエンド）テストの実行

Playwright を使用した E2E テストは、実際のブラウザを操作するため、**事前に API サーバーと UI アプリケーションを起動しておく必要があります。**

### 手順

#### ステップ 0: 既存サーバーの停止

テスト前に、既に起動している可能性のあるサーバープロセスを停止して、ポートの競合を防ぎます。

```bash
killall -9 uvicorn streamlit || true
```

#### ステップ 1: API サーバーの起動

まず、バックエンドの API サーバーをターミナルで起動します。

```bash
# プロジェクトのルートディレクトリで実行
uv run uvicorn api.main:app --reload --port 8000
```

このプロセスはバックグラウンドで実行するか、別のターミナルで起動したままにしてください。

#### ステップ 2: UI アプリケーションの起動

次に、フロントエンドの UI アプリケーションを別のターミナルで起動します。

```bash
# プロジェクトのルートディレクトリで実行
cd ui
uv run streamlit run main.py --server.port 8501
cd ..
```

このプロセスも同様に、バックグラウンドまたは別のターミナルで起動したままにします。

#### ステップ 3: Playwright テストの実行

API と UI が両方起動した状態で、メインのターミナルから以下のコマンドを実行します。

```bash
# E2Eテストを実行（ブラウザの動作が表示されます）
uv run pytest tests/test_e2e_product_journey.py --headed

# ブラウザのUIなしで実行（CI環境など）
uv run pytest tests/test_e2e_product_journey.py
```
