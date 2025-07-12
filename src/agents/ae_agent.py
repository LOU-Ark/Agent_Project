# src/agents/ae_agent.py
import logging
from src.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class AEAgent(BaseAgent):
    def __init__(self):
        logger.info("Initializing AEAgent...")
        logger.debug("Calling super().__init__ with persona_file='ae_persona.md'")
        super().__init__(persona_file="ae_persona.md")
        logger.info("AEAgent initialization complete.")