from PIL import Image
from worker.config import BASE_DIR
from .base import BaseStorage

class LocalStorage(BaseStorage):
    """Simple LocalStorage class that saves images to the generated/ folder."""
    
    def get_name(self) -> str:
        return "local"

    def save_image(self, filename: str, image: Image.Image) -> str:
        """Save the image to the local generated/ directory.
        
        Returns:
            String representing the path to the saved image file.
        """
        print("Saving Image")
        save_dir = BASE_DIR / "generated"
        save_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = save_dir / filename
        image.save(filepath, format="PNG")
        
        # We can return either a relative path or absolute path. Let's return the string representation of the filepath.
        # Returning relative path like f"generated/{filename}" or absolute path is fine. Let's return the relative path from base dir or absolute.
        # The prompt says: "Save inside generated/ Return saved path." So let's return a string representing the relative path from BASE_DIR, or the absolute path. Let's return the absolute path or str(filepath). Let's return the path relative to current working directory or absolute.
        # Actually, let's do: relative path to the workspace root, e.g., f"generated/{filename}", or absolute path. Either is fine. Let's do a relative path or absolute. Let's return a string of filepath: str(filepath.resolve()) to be perfectly unambiguous.
        return str(filepath.resolve())
