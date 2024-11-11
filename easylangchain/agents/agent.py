from typing import List, Optional
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.chat_models.tongyi import ChatTongyi



class Agent:
    def __init__(
        self, 
        tools: List, 
        model_type: str = "openai", 
        api_key: Optional[str] = None
    ):
        """Initialize EasyChain with tools and model selection
        
        Args:
            tools: List of tools to bind to the model
            model_type: "openai" or "tongyi"
            api_key: API key for the selected model
        """
        if model_type == "openai":
            self.llm = ChatOpenAI(api_key=api_key).bind_tools(tools)
        elif model_type == "tongyi":
            self.llm = ChatTongyi().bind_tools(tools)
        else:
            raise ValueError("model_type must be 'openai' or 'tongyi'")
        
        self.tools = {tool.__name__: tool for tool in tools}
        self.messages = [
            SystemMessage(content="检测需要用到哪些tool，并且对应的args。要求返回多个tools"),
        ]
    
    def query(self, text: str) -> str:
        """Process a query using the chain"""
        self.messages.append(HumanMessage(content=text))
        response = self.llm.invoke(text)
        self.messages.append(response)
        
        # Process tool calls
        for tool_call in response.tool_calls:
            selected_tool = self.tools[tool_call["name"].lower()]
            tool_msg = selected_tool.invoke(tool_call)
            self.messages.append(tool_msg)
        
        # Get final response
        response = self.llm.invoke(self.messages)
        return StrOutputParser().invoke(response)
