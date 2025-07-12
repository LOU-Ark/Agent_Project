# src/orchestrator.py
import logging
from pathlib import Path
from src.agents.ae_agent import AEAgent

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        logger.info("Initializing Orchestrator...")
        self.agent = None
        self.user_profile = ""
        try:
            logger.debug("Creating AEAgent instance...")
            self.agent = AEAgent()
            logger.info("AEAgent instance created successfully.")
            
            logger.debug("Loading user profile...")
            self.user_profile = self._load_knowledge("user_profile.md")
            logger.info("User profile loaded.")
        except Exception as e:
            logger.error(f"Failed to initialize Orchestrator: {e}", exc_info=True)
            raise

    def _load_knowledge(self, file_name: str) -> str:
        path = Path(__file__).parent / "knowledge" / file_name
        logger.debug(f"Attempting to load knowledge file from: {path}")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                logger.debug(f"Successfully loaded file: {file_name}")
                return content
        except FileNotFoundError:
            logger.error(f"Knowledge file not found at: {path}")
            return ""

    def run(self, user_message: str) -> str:
        logger.info(f"Orchestrator run method called with message: '{user_message}'")
        if not self.agent:
            logger.error("Cannot run because agent is not initialized.")
            return "申し訳ありません、システムの初期化に失敗したため応答できません。"

        logger.debug("Delegating task to agent.chat...")
        response = self.agent.chat(
            user_message=user_message,
            user_profile=self.user_profile
        )
        return response