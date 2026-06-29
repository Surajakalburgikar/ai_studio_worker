import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Settings:
    """Settings class to manage worker configuration."""
    
    def __init__(self):
        self.worker_name: str = os.getenv("WORKER_NAME", "default-worker")
        self.backend_url: str = os.getenv("BACKEND_URL", "http://localhost:8000")
        self.image_provider: str = os.getenv("IMAGE_PROVIDER", "mock")
        self.storage_provider: str = os.getenv("STORAGE_PROVIDER", "local")
        self.worker_version: str = os.getenv("WORKER_VERSION", "0.1.0")
        self.poll_interval: int = int(os.getenv("POLL_INTERVAL", "5"))

# Expose settings object
settings = Settings()
