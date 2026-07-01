import logging
from typing import Optional, Union
from worker.backend.client import BackendClient
from worker.models.job import GenerationJob
from worker.execution.result import ExecutionResult

logger = logging.getLogger(__name__)

class Reporter:
    """Reporter responsible for reporting job lifecycle events to the Backend."""
    
    def __init__(self, client: Optional[BackendClient] = None) -> None:
        self.client = client or BackendClient()

    def report_started(self, job: GenerationJob) -> None:
        """Report that the job has started processing (progress 0%)."""
        print("Job Started")
        self.client.update_job_progress(job.id, 0)

    def report_progress(self, job: GenerationJob, progress: int) -> None:
        """Report the job progress to the backend."""
        self.client.update_job_progress(job.id, progress)

    def report_completed(self, job: GenerationJob, execution_result: ExecutionResult) -> None:
        """Report that the job completed successfully."""
        print("Job Finished")
        self.client.complete_job(
            job_id=job.id,
            drive_file_id=execution_result.image_path,
            generation_time=execution_result.generation_time,
            provider=execution_result.provider
        )

    def report_failed(self, job: GenerationJob, error: Union[Exception, str]) -> None:
        """Report that the job has failed."""
        error_msg = str(error)
        print(f"Job Failed: {error_msg}")
        self.client.fail_job(job.id, error_msg)
