from abc import ABC, abstractmethod
from PIL import Image
from worker.models.job import GenerationJob

class BaseImageProvider(ABC):
    """Abstract base class for all image providers."""
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of the image provider."""
        pass

    @abstractmethod
    def generate(self, job: GenerationJob) -> Image.Image:
        """Generate an image based on the job prompt."""
        pass
