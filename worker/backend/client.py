import requests
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
