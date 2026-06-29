from abc import ABC, abstractmethod

class BaseImageProvider(ABC):
    """Abstract base class for all image providers."""
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of the image provider."""
        pass
