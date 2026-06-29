import time
from worker.config import settings
from worker.image_providers.mock import MockProvider
from worker.storage.local import LocalStorage
from worker.execution.result import ExecutionResult
from worker.models.job import GenerationJob

class Executor:
    """Orchestrates image generation and storage using configured providers."""
    
    def __init__(self) -> None:
        self.image_provider = self._resolve_image_provider()
        self.storage_provider = self._resolve_storage_provider()

    def _resolve_image_provider(self):
        provider_name = settings.image_provider
        if provider_name == "mock":
            return MockProvider()
        else:
            raise ValueError(f"Unknown image provider: {provider_name}")

    def _resolve_storage_provider(self):
        storage_name = settings.storage_provider
        if storage_name == "local":
            return LocalStorage()
        else:
            raise ValueError(f"Unknown storage provider: {storage_name}")

    def execute(self, job: GenerationJob) -> ExecutionResult:
        """Executes a GenerationJob by generating and storing the image.
        
        Returns:
            ExecutionResult containing the outcome.
        """
        filename = job.filename or f"scene_{job.scene_id}_shot_{job.shot_number}.png"
        
        try:
            start_time = time.time()
            image = self.image_provider.generate(job)
            generation_time = time.time() - start_time
            
            output_path = self.storage_provider.save_image(filename, image)
            
            return ExecutionResult(
                status="success",
                provider=self.image_provider.get_name(),
                filename=filename,
                output_path=output_path,
                generation_time=generation_time,
                metadata={
                    "prompt": job.prompt,
                    "scene_id": job.scene_id,
                    "shot_number": job.shot_number,
                }
            )
        except Exception as e:
            return ExecutionResult(
                status="failed",
                provider=self.image_provider.get_name(),
                filename=filename,
                output_path="",
                generation_time=0.0,
                error_message=str(e)
            )
