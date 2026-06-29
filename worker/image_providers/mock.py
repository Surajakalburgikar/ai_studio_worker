from .base import BaseImageProvider

class MockProvider(BaseImageProvider):
    """Simple MockProvider for testing."""
    
    def get_name(self) -> str:
        return "mock"
