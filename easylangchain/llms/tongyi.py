import os
from .base import BaseLLM, check_params


class ChatTongyi(BaseLLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        from langchain_community.chat_models.tongyi import ChatTongyi
        
        os.environ["DASHSCOPE_API_KEY"] = kwargs["api_key"]
        filtered_kwargs = check_params(ChatTongyi, **kwargs)
        self.llm = ChatTongyi(**filtered_kwargs)

