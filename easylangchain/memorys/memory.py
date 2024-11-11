from typing import Dict
from easylangchain.messages import MESSAGE_TYPE, MESSAGES_TYPE, SystemMessage, AIMessage, HumanMessage, _convert_messages


class Memory:
    def __init__(
        self, 
        has_system_message: bool = True,
        messages: MESSAGES_TYPE = [],
    ):
        """Memory class"""
        self.has_system_message = has_system_message
        if len(messages) > 0 and not isinstance(messages[0], SystemMessage):
            raise ValueError("The first message must be a SystemMessage or set to an empty list!")
        
        if not messages and self.has_system_message:
            messages = [SystemMessage(content = "You are a helpful assistant. Please answer me in the same language as the user requests last time.")]
        
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
        self.messages = []
        print("Your memory has been cleared. Make sure you deploy .set_initial_message() to set the initial system message.")
    
    def delete(self, index: int):
        """Delete the message by index"""
        self.messages.pop(index)
        return True
    
    

