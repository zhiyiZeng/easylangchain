
class Logger:
    """Logger(not implemented)"""
    def __init__(self, log_level: str = "INFO"):
        self.log_level = log_level
        
    def log(self, message: str):
        print(message)

