from .base import BaseStorage

class LocalStorage(BaseStorage):
    """Simple LocalStorage class that returns its name."""
    
    def get_name(self) -> str:
        return "local"
