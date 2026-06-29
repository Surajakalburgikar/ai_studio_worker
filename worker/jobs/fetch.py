from typing import Optional
from worker.backend.client import BackendClient
from worker.models.job import GenerationJob

class JobFetcher:
    """Class to fetch generation jobs from the backend."""
    
    def __init__(self, client: Optional[BackendClient] = None) -> None:
        self.client = client or BackendClient()

    def fetch_job(self) -> Optional[GenerationJob]:
        """Fetch the next pending generation job from the backend.
        
        Returns:
            GenerationJob if a job exists, None otherwise.
        """
        job_data = self.client.get_next_job()
        if job_data:
            return GenerationJob.from_dict(job_data)
        return None
