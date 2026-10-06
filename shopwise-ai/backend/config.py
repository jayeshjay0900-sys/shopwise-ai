from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    port: int = int(os.getenv("PORT", "3000"))
    frontend_dist: str = os.getenv("FRONTEND_DIST", "frontend/dist")


settings = Settings()
