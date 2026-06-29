from abc import ABC, abstractmethod

class BaseStorage(ABC):
    """Abstract base class for all storage backends."""
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of the storage provider."""
        pass
