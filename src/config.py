"""Application settings loaded from environment / .env file."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

# Load .env file at import time
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


@dataclass
class Settings:
    llm_provider: str = "anthropic"          # "anthropic" | "openai"
    llm_model: str = "claude-sonnet-4-5-20250929"
    llm_temperature: float = 0.2

    anthropic_api_key: str = ""
    openai_api_key: str = ""

    supabase_url: str = ""
    supabase_key: str = ""

    vector_store_type: str = "pgvector"      # "pgvector" | "pinecone"
    pinecone_api_key: str = ""

    log_level: str = "INFO"
    max_retries: int = 2
    token_budget_per_agent: int = 8000

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            llm_provider=os.getenv("LLM_PROVIDER", "anthropic"),
            llm_model=os.getenv("LLM_MODEL", "claude-sonnet-4-5-20250929"),
            llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0.2")),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            supabase_url=os.getenv("SUPABASE_URL", ""),
            supabase_key=os.getenv("SUPABASE_KEY", ""),
            vector_store_type=os.getenv("VECTOR_STORE_TYPE", "pgvector"),
            pinecone_api_key=os.getenv("PINECONE_API_KEY", ""),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            max_retries=int(os.getenv("MAX_RETRIES", "2")),
            token_budget_per_agent=int(os.getenv("TOKEN_BUDGET_PER_AGENT", "8000")),
        )

    @property
    def has_llm_key(self) -> bool:
        if self.llm_provider == "anthropic":
            return bool(self.anthropic_api_key)
        return bool(self.openai_api_key)


settings = Settings.from_env()
