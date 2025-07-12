import os
from dotenv import load_dotenv

# プロジェクトルートの.envファイルから環境変数を読み込む
load_dotenv()

# GeminiのAPIキー
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 使用するGeminiモデル名 (最新のFlashモデルを推奨)
GEMINI_MODEL_NAME = "gemini-2.5-pro"