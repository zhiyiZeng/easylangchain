#!/bin/bash

# Create directory structure
mkdir -p ./easylangchain/{tools,utils}

# Create setup.py
cat > easylangchain/setup.py << 'EOL'
from setuptools import setup, find_packages

setup(
    name="easylangchain",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain-community",
        "langchain-core",
        "langchain-openai",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A simplified wrapper around LangChain for easy tool usage",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/easylangchain", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
EOL

# Create tools/weather.py

cat > ./easylangchain/tools/weather.py << 'EOL'
from langchain_core.tools import tool

weathers = {
    "北京": {"2024-11-10": "晴", "2024-11-11": "多云"},
    "上海": {"2024-11-10": "小雨", "2024-11-11": "多云"},
}

@tool
def get_weather(location: str, date: str = "2024-11-10") -> str:
    """Get the weather of a location on a specific date.
    Args:
        location: The location to get the weather of.
        date: The date to get the weather of. defaults to 2024-11-10.
    """
    return weathers[location][date]

@tool
def get_north_or_south(location: str,) -> str:
    """获取是北方城市还是南方城市
    """
    return {
        "北京": "north",
        "上海": "south"
    }[location]
EOL

# Create utils/api.py
cat > ./easylangchain/utils/api.py << 'EOL'
import os
from typing import Optional

def get_api_token(token_name: str) -> Optional[str]:
    """Get API token from environment variables"""
    return os.getenv(token_name)

def set_dashscope_token(token: str) -> None:
    """Set DashScope API token"""
    os.environ["DASHSCOPE_API_KEY"] = token
EOL

# Create chain.py
cat > ./easylangchain/chain.py << 'EOL'
from typing import List, Optional
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.chat_models.tongyi import ChatTongyi

class EasyChain:
    def __init__(self, tools: List, model_type: str = "openai", api_key: Optional[str] = None):
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
EOL

# Create __init__.py files
cat > ./easylangchain/__init__.py << 'EOL'
from .chain import EasyChain
from .tools.weather import get_weather, get_north_or_south
from .utils.api import get_api_token, set_dashscope_token

__all__ = [
    "EasyChain",
    "get_weather",
    "get_north_or_south",
    "get_api_token",
    "set_dashscope_token",
]
EOL

touch ./easylangchain/tools/__init__.py
touch ./easylangchain/utils/__init__.py

# Create README.md
cat > ./README.md << 'EOL'
# EasyLangChain

A simplified wrapper around LangChain for easy tool usage.

## Installation
