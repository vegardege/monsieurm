import os
from typing import Optional

from pydantic import BaseModel


class MissingConfig(Exception):
    pass


class Config(BaseModel):
    mistral_api_key: str
    slack_bot_token: Optional[str]


def load_config() -> Config:
    """Load config from environment variables, raise errors if required vars
    are missing."""
    try:
        return Config(
            mistral_api_key=os.environ["MONSIEURM_MISTRAL_API_KEY"],
            slack_bot_token=os.environ.get("MONSIEURM_SLACK_TOKEN"),
        )
    except KeyError as e:
        raise MissingConfig(f"Missing env var: {e}")
