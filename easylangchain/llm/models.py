import os
from typing import List, Optional, Dict
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


class BaseLLM:
    def bind_tools(self, tools: List):
        return self.llm.bind_tools(tools)
    
    def invoke(self, messages: List | Dict):
        return self.llm.invoke(messages)

    def parse_response(self, response, format_type: str = "str"):
        if format_type == "str":
            str_parser = StrOutputParser()
            return str_parser.invoke(response)
        else:
            raise ValueError("not implemented, you can implement it by rewrite this function.")
        
        
class ChatTongyi(BaseLLM):
    def __init__(self, **kwargs):
        from langchain_community.chat_models.tongyi import ChatTongyi
        
        os.environ["DASHSCOPE_API_KEY"] = kwargs["api_key"]
        kwargs.pop("api_key")
        
        self.llm = ChatTongyi(**kwargs)
