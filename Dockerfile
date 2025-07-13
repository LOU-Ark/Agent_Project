# ベースとなる公式Pythonイメージを選択 (変更なし)
FROM python:3.10-slim

# --- NEW: セキュリティ向上のための非rootユーザー設定 ---
# アプリケーションを実行するための専用ユーザーを作成
RUN useradd --create-home --shell /bin/bash appuser
# 作業ディレクトリを作成し、所有者をappuserに変更
WORKDIR /app
RUN chown appuser:appuser /app
# これ以降のコマンドはappuserとして実行される
USER appuser
# ---

# Cloud Runが提供するPORT環境変数を利用する
# ENV PORT 8080 # この行はCMDで直接$PORTを使うため、必須ではないが残しても良い

# 依存関係ファイルをコピー
COPY requirements.txt ./
# インストール
RUN pip install --no-cache-dir --user -r requirements.txt

# アプリケーションの全コードをコピー
COPY . .

# --- MODIFIED: 本番環境に最適化された起動コマンド ---
# exec: Gunicornがコンテナのメインプロセスとなり、シグナルを正しく受け取れるようにする
# --bind :$PORT: Cloud Runから提供されるポートを動的に使用する
# --workers 1 --threads 8: シングルコア環境での推奨設定
# --timeout 0: AIの応答生成が長くても、ワーカーがタイムアウトしないようにする
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 "web.app:app"