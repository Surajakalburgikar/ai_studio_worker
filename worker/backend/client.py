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

    def update_job_progress(self, job_id: int, progress: int) -> Optional[Dict[str, Any]]:
        """Update progress percentage of a job on the backend."""
        try:
            response = requests.patch(
                f"{self.backend_url}/jobs/{job_id}/progress",
                json={"progress": progress},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None

    def complete_job(self, job_id: int, drive_file_id: Optional[str], generation_time: Optional[float]) -> Optional[Dict[str, Any]]:
        """Mark a job as completed on the backend."""
        try:
            response = requests.post(
                f"{self.backend_url}/jobs/{job_id}/complete",
                json={"drive_file_id": drive_file_id, "generation_time": generation_time},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None

    def fail_job(self, job_id: int, error_message: str) -> Optional[Dict[str, Any]]:
        """Mark a job as failed on the backend."""
        try:
            response = requests.post(
                f"{self.backend_url}/jobs/{job_id}/failed",
                json={"error_message": error_message},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None
