# src/agents/base_agent.py
import logging
from pathlib import Path
import google.genai as genai
from config.settings import GEMINI_API_KEY, GEMINI_MODEL_NAME

logger = logging.getLogger(__name__)

class BaseAgent:
    def __init__(self, persona_file: str, model: str = None):
        logger.info(f"Initializing BaseAgent with persona: '{persona_file}'")
        if not GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY is not set or empty in .env file!")
            raise ValueError("Gemini APIキーが設定されていません。.envファイルを確認してください。")
        else:
            logger.debug("GEMINI_API_KEY loaded successfully.")
        
        self.model_name = model or GEMINI_MODEL_NAME
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.chat_session = None
        logger.debug(f"genai.Client initialized for model: {self.model_name}")
        
        try:
            project_root = Path(__file__).parent.parent.parent
            persona_path = project_root / 'src' / 'knowledge' / persona_file
            logger.debug(f"Attempting to load persona from path: {persona_path}")
            with open(persona_path, 'r', encoding='utf-8') as f:
                self.persona = f.read()
            logger.info("Persona loaded successfully.")
        except FileNotFoundError:
            logger.error(f"Persona file not found at {persona_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading persona file: {e}", exc_info=True)
            raise

    def chat(self, user_message: str, user_profile: str = "") -> str:
        """
        ユーザーメッセージを受け取り、継続的な会話セッションで応答を生成します。
        """
        logger.info(f"BaseAgent.chat called with message: '{user_message}'")
        try:
            # 1. セッションがまだ始まっていない場合（最初のメッセージ）
            if self.chat_session is None:
                logger.info("No active chat session found. Creating a new one.")

                # システムプロンプトを構築
                system_prompt = f"""
# 指示
あなたは以下のペルソナになりきって、ユーザーと対話してください。
**最重要ルール：応答は常に簡潔に、およそ100文字程度で要約して回答してください。**

# あなたのペルソナ
{self.persona}

# ユーザーに関する情報
{user_profile}
""".strip()            
                logger.debug("--- System Prompt for API Call ---")
                logger.debug(system_prompt)
                logger.debug("---------------------------------")
                
                # 新しいチャットセッションをインスタンス変数に格納
                self.chat_session = self.client.chats.create(model=self.model_name)
                
                # 最初のメッセージとしてシステムプロンプトを送信
                self.chat_session.send_message(system_prompt)

            # 2. ユーザーからのメッセージを、既存または新規のセッションに送信
            logger.info("Sending user message to the chat session...")
            response = self.chat_session.send_message(user_message)
            
            logger.info("Received response from Gemini API.")
            logger.debug(f"API response text: '{response.text[:80]}...'")
            return response.text
            
        except Exception as e:
            logger.error(f"An error occurred during Gemini API call: {e}", exc_info=True)
            return "申し訳ありません、現在AIとの通信で問題が発生しています。"