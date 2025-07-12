# web/app.py
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, jsonify
from src.orchestrator import Orchestrator

# --- ↓↓↓ NEW LOGGING SETUP ↓↓↓ ---
# 1. ロガーの取得
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # ロガー自体のレベルはDEBUGに設定

# 2. ログのフォーマットを定義
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# 3. コンソールハンドラの設定 (INFOレベル以上を表示)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(log_format)

# 4. ファイルハンドラの設定 (DEBUGレベル以上をファイルに保存)
# ログファイルはプロジェクトルートに `debug.log` として作成される
# maxBytes=1MB, 3世代までバックアップ
file_handler = RotatingFileHandler('debug.log', maxBytes=1024*1024, backupCount=3, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_format)

# 5. Werkzeug(Flaskの内部サーバー)のロガーも同様に設定し、重複を防ぐ
werkzeug_logger = logging.getLogger('werkzeug')
# 既存のハンドラをクリア
werkzeug_logger.handlers.clear()

# 6. 作成したハンドラをロガーに追加
logger.addHandler(console_handler)
logger.addHandler(file_handler)
werkzeug_logger.addHandler(console_handler)
werkzeug_logger.addHandler(file_handler)

# 7. Flaskのデフォルトロガーを無効化
app_logger = logging.getLogger('flask.app')
app_logger.handlers.clear()
app_logger.propagate = True
# --- ↑↑↑ NEW LOGGING SETUP ↑↑↑ ---

app = Flask(
    __name__,
    static_folder='static',      # 'static' フォルダの場所を指定
    template_folder='templates'  # 'templates' フォルダの場所を指定
)

# Orchestratorの初期化ログはそのまま
logger.info("Initializing application and Orchestrator...")
orchestrator = Orchestrator()
logger.info("Orchestrator initialization complete.")

@app.route('/')
def index():
    logger.debug("Serving index.html")
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    logger.info("Received request on /chat endpoint")
    if not orchestrator or not orchestrator.agent:
        logger.error("Orchestrator or its agent is not initialized.")
        return jsonify({'agent_message': 'サーバーエラー: Orchestratorが初期化されていません。'}), 500

    user_message = request.json.get('message')
    logger.debug(f"User message received: '{user_message}'")
    if not user_message:
        logger.warning("Received an empty message.")
        return jsonify({'error': 'Message is empty'}), 400

    try:
        logger.info("Calling orchestrator.run()...")
        agent_response = orchestrator.run(user_message)
        logger.info(f"Response received from orchestrator: '{agent_response[:80]}...'")
        return jsonify({
            'agent_message': agent_response,
            'agent_icon': '/static/images/ae.png' # エルのアイコンパスを指定
        })
    except Exception as e:
        logger.error(f"An unexpected error occurred in /chat endpoint: {e}", exc_info=True)
        return jsonify({'agent_message': '申し訳ありません、サーバー内部で予期せぬエラーが発生しました。'}), 500

# logging設定を他のモジュールと共有するため、app自体のロガーは直接使わない
# if __name__ == '__main__': ... の部分は run.py にあるのでここでは不要