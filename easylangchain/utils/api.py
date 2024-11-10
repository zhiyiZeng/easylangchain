import os
from typing import Optional

def get_api_token(token_name: str) -> Optional[str]:
    """Get API token from environment variables"""
    return os.getenv(token_name)

def set_dashscope_token(token: str) -> None:
    """Set DashScope API token"""
    os.environ["DASHSCOPE_API_KEY"] = token
