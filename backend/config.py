import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class Config:
    """Configuration settings for the RAG system (simplified - no vector DB)"""

    # Anthropic API settings
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = "claude-sonnet-4-20250514"

    # Profile settings
    PROFILE_PATH: str = "../yuanyuan_li_profile.json"  # Path to profile JSON

    # Conversation settings
    MAX_HISTORY: int = 2  # Number of conversation message pairs to remember


config = Config()
