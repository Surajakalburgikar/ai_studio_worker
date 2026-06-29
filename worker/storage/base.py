from abc import ABC, abstractmethod
from PIL import Image

class BaseStorage(ABC):
    """Abstract base class for all storage backends."""
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of the storage provider."""
        pass

    @abstractmethod
    def save_image(self, filename: str, image: Image.Image) -> str:
        """Save the image to the storage backend and return the saved path."""
        pass
