import os
from .base import BaseLLM, check_params


class ChatOpenAI(BaseLLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from langchain_openai import ChatOpenAI
        filtered_kwargs = check_params(ChatOpenAI, **kwargs)
        self.llm = ChatOpenAI(**filtered_kwargs)
    