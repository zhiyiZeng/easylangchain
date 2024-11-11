from typing import List, Optional, Dict
from langchain_core.messages import SystemMessage, HumanMessage


class Memory:
    def __init__(
        self, 
        has_memory: bool = False, 
        messages: List = []
    ):
        self.has_memory = has_memory
        self.messages = messages
        if not messages:
            messages = [SystemMessage(content = "You are a helpful assistant.")]
            self.update(messages)
        
    def update(self, messages: List | Dict):
        """Update the memory with new messages
        
        Args:
            messages (List | Dict): _description_
        """
        if not self.has_memory:
            return
        
        if isinstance(messages, List):
            self.messages.extend(messages)
        else:
            self.messages.append(messages)

    def get(self, index: int = -1):
        if index == -1:
            return self.messages
        else:
            return self.messages[index]

    def clear(self):
        self.messages = []

    def delete(self, index: int):
        return 
    

