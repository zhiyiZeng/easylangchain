import os
from typing import List, Dict
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from easylangchain.memorys import Memory

def check_params(langchain_model, **kwargs):
    """Check if kwargs match the parameter types of the model"""
    accept_params = langchain_model.__init__.__annotations__

    accept_params.update({
        "api_key": str,
        "base_url": str,
        "model": str,
        "temperature": float,
        "max_tokens": int,
    })

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


class BaseLLM:
    
    RESPONSE_FORMAT_TYPES = {
        "str": StrOutputParser(),
        "json": JsonOutputParser()
    }
    
    def __init__(self, **kwargs):
        self.tools = {}
        self.has_tools = False
        self.has_memory = False
        
        if kwargs.get("has_memory", True) or "messages" in kwargs:
            self.has_memory = True

        # NOTE if has_memory is True, history_memory is used to store the history messages
        # NOTE otherwise, history_memory will only be used to store one round conversation, same as active_memory.
        self.history_memory = Memory(
            messages = kwargs.get("messages", []),
        )
        
        # NOTE active_memory is used to store the current round conversation.
        self.active_memory = Memory(
            has_system_message = False,
        )

    def reset_memory(self):
        """Reset the memory"""
        self.history_memory = Memory()
        self.active_memory = Memory(has_system_message = False)
        
    def bind_tools(self, tools: List):
        """Bind tools to the model"""
        self.llm = self.llm.bind_tools(tools)
        self.tools = {tool.name: tool for tool in tools}
        self.has_tools = True
        return self
    
    def invoke(self, messages: str | Dict | List):
        """Invoke the model
        
        Args:
            messages: The messages to invoke the model. 
                        - If set to a string, it will be converted to a HumanMessage as default.
                        - If set to a dict, it accepts openai message format, such as:
                        {"role": "user", "content": "Hello, how are you?"}. 
                        The role can be "system", "assistant", "user", "tool", "function".
                        - If set to a list, it accepts a list of messages.
        """
        if not self.has_memory:
            self.reset_memory()
            
        self.history_memory.update(messages)
        self.active_memory.update([self.history_memory.get(-1)])
        
        if self.has_tools:
            self.history_memory.update(HumanMessage(content = "response with json format if any tools are possible. If not, don't apologize or output unrelated information."))
            
        response = self.llm.invoke(self.history_memory.get())
        self.history_memory.update(response)
        
        if self.has_tools:
            if response.invalid_tool_calls:
                print("Invalid tool calls!", response.invalid_tool_calls)
            
            elif len(response.tool_calls) > 0:
                self.active_memory.update(response)
                self.tools_invoke(response.tool_calls)

                # Get final response
                response = self.llm.invoke(self.active_memory.get())
                self.history_memory.update(response)
                self.active_memory.update(response)
            
        return response
    
    def tools_invoke(self, tool_calls: List[Dict]):
        """Invoke tools and update the memory"""
        for tool_call in tool_calls:
            selected_tool = self.tools[tool_call["name"].lower()]
            tool_msg = selected_tool.invoke(tool_call)
            self.history_memory.update(tool_msg)
            self.active_memory.update(tool_msg)
        
        return 
    
    def parse_response(self, response, format_type: str = "str"):
        """Parse the response"""
        format_parser = self.RESPONSE_FORMAT_TYPES.get(format_type)
        if format_parser is None:
            raise ValueError("not implemented, you can implement it by updating self.RESPONSE_FORMAT_TYPES using pure python dict grammar.")
        return format_parser.invoke(response)
