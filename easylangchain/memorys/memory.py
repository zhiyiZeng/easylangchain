from typing import Dict, List
from easylangchain.messages import MESSAGE_TYPE, MESSAGES_TYPE, SystemMessage, AIMessage, HumanMessage, _convert_messages


class Memory:
    def __init__(
        self, 
        has_system_message: bool = True,
        messages: MESSAGES_TYPE = [],
        max_length: int = 100
    ):
        """Memory class"""
        self.max_length = max_length
        self.has_system_message = has_system_message
        
        if not isinstance(messages, List):
            raise ValueError("The messages when Memory is initialized must be a list of messages!")
        
        self.initial_messages = "You are a helpful assistant. Use the same language as the user requests last time."
        if not messages and self.has_system_message:
            messages = [SystemMessage(content = self.initial_messages)]
        else:
            messages.insert(0, SystemMessage(content = self.initial_messages))

        self.messages = _convert_messages(messages)
        
    def update(self, messages: str | MESSAGE_TYPE | MESSAGES_TYPE):
        """Update the memory with new messages
        """
        
        # NOTE if messages is a string, it will be converted to a HumanMessage as default
        if isinstance(messages, str):
            messages = [HumanMessage(content = messages)]
        
        messages = [messages] if isinstance(messages, MESSAGE_TYPE) else messages
        self.messages.extend(_convert_messages(messages))

    def get(self, index: int = None):
        """Get the messages by index
        Args:
            index: The index of the message to get. If set to None, return all messages.
        """
        if index is None:
            return self.messages
        else:
            return self.messages[index]

    def clear(self):
        """Clear the messages"""
        self.messages = _convert_messages(messages)
    
    def delete(self, index: int):
        """Delete the message by index"""
        self.messages.pop(index)
        return True
    
    

