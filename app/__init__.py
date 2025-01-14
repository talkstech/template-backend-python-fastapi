import os
from typing import List

from loguru import logger
from pydantic import BaseSettings


class Config(BaseSettings):
    enable_docs: bool = True
    profile_endpoints: bool = True
    cors_origins: List[str] = ["*"]


stage = os.environ.get("STAGE")
file = f".env.{stage.lower()}" if stage else ".env.dev"


config = Config(_env_file=file, _env_file_encoding="utf-8")  # type: ignore[call-arg]


logger.info(f"Config: {config}")
