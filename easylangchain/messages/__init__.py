from typing import List, Dict
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, ToolMessage, FunctionMessage

MESSAGE_TYPE = Dict | SystemMessage | AIMessage | HumanMessage | ToolMessage | FunctionMessage
MESSAGES_TYPE = List[Dict] | List[SystemMessage | AIMessage | HumanMessage]


ROLES = {
    "system": SystemMessage,
    "assistant": AIMessage,
    "user": HumanMessage,
    "tool": ToolMessage,
    "function": FunctionMessage,
}


def _convert_dict_to_message(message: MESSAGE_TYPE):
    """Convert a dictionary message to a langchain Message object"""
    role = message.get("role", "user").lower()
    content = message.get("content", "")
    
    assert role in ROLES, f"Role {role} is not supported" 
    return ROLES[role](content=content) 


def _convert_messages(messages: MESSAGES_TYPE):
    """Convert a list of messages to langchain Message objects"""
    converted = []
    for message in messages:
        if isinstance(message, dict):
            converted.append(_convert_dict_to_message(message))
        else:
            converted.append(message)
    return converted

