from PIL import Image, ImageDraw
from worker.models.job import GenerationJob
from .base import BaseImageProvider

class MockProvider(BaseImageProvider):
    """Simple MockProvider for testing."""
    
    def get_name(self) -> str:
        return "mock"

    def generate(self, job: GenerationJob) -> Image.Image:
        """Generate a placeholder mock image with text.
        
        Requirements:
        - 800x600 size
        - Dark background (RGB 30, 30, 30)
        - White text (RGB 255, 255, 255)
        - Displays:
          - "AI Studio Mock Image"
          - Filename
          - First 100 characters of prompt
        """
        print("Generating Image")
        # Create a dark image
        image = Image.new("RGB", (800, 600), color=(30, 30, 30))
        draw = ImageDraw.Draw(image)
        
        # Get info to draw
        filename = job.filename or f"scene_{job.scene_id}_shot_{job.shot_number}.png"
        prompt_text = job.prompt[:100]
        
        text = (
            "AI Studio Mock Image\n\n"
            f"Filename: {filename}\n"
            f"Prompt: {prompt_text}"
        )
        
        # Draw the text at (50, 50) using default font
        draw.text((50, 50), text, fill=(255, 255, 255))
        return image
