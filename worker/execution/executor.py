import time
from worker.config import settings
from worker.image_providers.mock import MockProvider
from worker.image_providers.flux_provider import FluxProvider
from worker.storage.local import LocalStorage
from worker.execution.result import ExecutionResult
from worker.models.job import GenerationJob

class Executor:
    """Orchestrates image generation and storage using configured providers."""
    
    def __init__(self) -> None:
        self.image_provider = self._resolve_image_provider()
        self.storage_provider = self._resolve_storage_provider()

    def _resolve_image_provider(self):
        """Resolve the configured image provider.

        Provider selection is the Executor's responsibility.
        Future sprint will migrate this to a Provider Registry
        without changing the Executor's public API.
        """
        provider_name = settings.image_provider
        if provider_name == "mock":
            return MockProvider()
        elif provider_name == "flux":
            return FluxProvider()
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
        import json
        
        spec = None
        try:
            spec = json.loads(job.prompt)
        except Exception:
            pass

        image_provider = self.image_provider
        filename = job.filename

        if spec and isinstance(spec, dict) and "compiled_positive_prompt" in spec:
            provider_name = spec.get("provider", "flux").lower().strip()
            if provider_name == "flux":
                image_provider = FluxProvider()
            elif provider_name == "mock":
                image_provider = MockProvider()
            
            job.prompt = spec["compiled_positive_prompt"]
            job.negative_prompt = spec.get("compiled_negative_prompt")
            if spec.get("output_configuration", {}).get("filename"):
                filename = spec["output_configuration"]["filename"]
                job.filename = filename
                
            job.generation_spec = spec

        if not filename:
            filename = f"scene_{job.scene_id}_shot_{job.shot_number}.png"
            job.filename = filename

        try:
            start_time = time.time()
            image = image_provider.generate(job)
            generation_time = time.time() - start_time
            
            output_path = self.storage_provider.save_image(filename, image)
            
            return ExecutionResult(
                success=True,
                provider=image_provider.get_name(),
                generation_time=generation_time,
                image_path=output_path,
                message="Image generated successfully"
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                provider=image_provider.get_name(),
                generation_time=0.0,
                image_path="",
                message=str(e)
            )
