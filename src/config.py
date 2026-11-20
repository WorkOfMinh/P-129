from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_name: str = "AI20K Agent"
    app_env: Literal["development", "production", "test"] = "development"
    app_port: int = Field(default=8000, ge=1, le=65535)
    app_host: str = "0.0.0.0"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    cors_origins: str = "http://localhost:3000"

    # LLM — cascade router: mỗi task type một model (bài học cost-management:
    # không đốt model mạnh cho việc classify). Judge PHẢI khác model generator
    # để tránh self-preference bias (bài học team 002 — eval judge riêng).

    llm_provider: Literal["openai"] = "openai"  # hiện chỉ hỗ trợ OpenAI (langchain_openai)
    openai_api_key: str = ""
    
    openai_max_tokens: int = Field(default=2048, ge=1, le=128000)  # giới hạn độ dài output
    model_classify: str = "gpt-6-luna"  # cheap: classify / route / quyết định tool
    model_generate: str = "gpt-6.1-sol"  # strong: sinh câu trả lời cuối
    model_judge: str = "gpt-6.1-terra"  # judge: khác model_generate mặc định

    # Agent loop — escape hatch chống loop vô hạn (bài học team 011:
    # luôn phải có một đường tới END dù LLM cứ đòi gọi tool mãi)
    agent_max_iterations: int = Field(default=8, ge=1, le=50)

    database_url: str = "sqlite:///./data/app.db" # Database
    chroma_persist_dir: str = "./data/chroma" # Vector Store


@lru_cache
def get_settings() -> Settings:
    return Settings()
