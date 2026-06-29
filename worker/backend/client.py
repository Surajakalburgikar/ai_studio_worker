import requests
from typing import Optional, Dict, Any
from worker.config import settings

class BackendClient:
    """Client for communicating with the main AI Studio Backend."""
    
    def __init__(self) -> None:
        self.backend_url: str = settings.backend_url

    def check_connection(self) -> bool:
        """Check connection to the backend root URL.
        
        Returns:
            True if status code is 200, False otherwise.
        """
        try:
            response = requests.get(self.backend_url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_next_job(self) -> Optional[Dict[str, Any]]:
        """Fetch the next pending generation job from the backend.
        
        Returns:
            Dictionary representing the job if found, None if no jobs found (404)
            or on other errors/exceptions.
        """
        try:
            response = requests.get(f"{self.backend_url}/jobs/next", timeout=5)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                return None
        except requests.RequestException:
            return None
