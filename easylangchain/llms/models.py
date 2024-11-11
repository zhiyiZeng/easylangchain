import os
from typing import List, Optional, Dict
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from easylangchain.memorys import Memory


class BaseLLM:
    def __init__(self, **kwargs):
        self.tools = {}
        self.has_tools = False
        self.has_memory = False
        
        if kwargs.get("has_memory", True) or "messages" in kwargs:
            self.has_memory = True
    
        self.memory = Memory(
            has_memory = self.has_memory, 
            messages = kwargs.get("messages", [])
        )
        
    def check_params(self, model, **kwargs):
        """Check if kwargs match the parameter types of the model"""
        accept_params = model.__init__.__annotations__
        filtered_kwargs = {}
        for key, value in kwargs.items():
            if key in accept_params:
                # Check if value matches the expected type
                expected_type = accept_params[key]
                try:
                    # Attempt type validation
                    if isinstance(value, expected_type):
                        filtered_kwargs[key] = value
                except TypeError:
                    # Handle complex types that can't be directly checked
                    filtered_kwargs[key] = value
        
        return filtered_kwargs
    
    def bind_tools(self, tools: List):
        """Bind tools to the model"""
        self.llm = self.llm.bind_tools(tools)
        self.tools = {tool.name: tool for tool in tools}
        self.has_tools = True
        return self
    
    def invoke(self, messages: List | Dict):
        """Invoke the model"""
        # TODO 这里要做个过滤么？
        self.memory.update(messages)
        response = self.llm.invoke(self.memory.get())
        self.memory.update(response)
        
        if self.has_tools and len(response.tool_calls) > 0:
            self.tools_invoke(response.tool_calls)
            # Get final response
            response = self.llm.invoke(self.memory.get())
            
        return response
    
    def tools_invoke(self, tool_calls: List[Dict]):
        """Invoke tools and update the memory"""
        for tool_call in tool_calls:
            selected_tool = self.tools[tool_call["name"].lower()]
            tool_msg = selected_tool.invoke(tool_call)
            self.memory.update(tool_msg)
        
        return 
    
    def parse_response(self, response, format_type: str = "str"):
        """Parse the response"""
        if format_type == "str":
            str_parser = StrOutputParser()
            return str_parser.invoke(response)
        else:
            raise ValueError("not implemented, you can implement it by rewrite this function.")
    
        
class ChatOpenAI(BaseLLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from langchain_openai import ChatOpenAI
        filtered_kwargs = self.check_params(ChatOpenAI, **kwargs)
        self.llm = ChatOpenAI(**filtered_kwargs)
    
    
class ChatTongyi(BaseLLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        from langchain_community.chat_models.tongyi import ChatTongyi
        
        os.environ["DASHSCOPE_API_KEY"] = kwargs["api_key"]
        filtered_kwargs = self.check_params(ChatTongyi, **kwargs)
        self.llm = ChatTongyi(**filtered_kwargs)
    