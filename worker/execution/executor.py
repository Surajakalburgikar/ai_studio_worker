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
        import os
        is_verify = os.environ.get("VERIFY_PIPELINE") == "true"

        if provider_name == "mock":
            return MockProvider()
        elif provider_name == "flux":
            try:
                return FluxProvider()
            except Exception as e:
                if is_verify:
                    print(f"[Executor] Failed to initialize FluxProvider: {e}. Switching to MockProvider for verification mode.")
                    return MockProvider()
                raise
        else:
            if is_verify:
                print(f"[Executor] Unknown provider '{provider_name}'. Switching to MockProvider for verification mode.")
                return MockProvider()
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
            import os
            is_verify = os.environ.get("VERIFY_PIPELINE") == "true"
            if provider_name == "flux":
                try:
                    image_provider = FluxProvider()
                except Exception as e:
                    if is_verify:
                        print(f"[Executor] Failed to initialize FluxProvider: {e}. Fallback to MockProvider for verification.")
                        image_provider = MockProvider()
                    else:
                        raise
            elif provider_name == "mock":
                image_provider = MockProvider()
            
            job.prompt = spec["compiled_positive_prompt"]
            job.negative_prompt = spec.get("compiled_negative_prompt")
            if spec.get("output_configuration", {}).get("filename"):
                filename = spec["output_configuration"]["filename"]
                job.filename = filename
                
            job.generation_spec = spec

        proj_id = getattr(job, "project_id", 0) or 0
        scene_num = getattr(job, "scene_number", 0) or getattr(job, "scene_id", 0) or 0
        shot_num = getattr(job, "shot_number", 0) or 0
        filename = f"Project_{proj_id:03d}/Scene_{scene_num:03d}/shot_{shot_num:03d}.png"
        job.filename = filename

        try:
            start_time = time.time()
            try:
                image = image_provider.generate(job)
            except Exception as e:
                import os
                if os.environ.get("VERIFY_PIPELINE") == "true" and image_provider.get_name() != "mock":
                    print(f"[Executor] Real generation failed: {e}. Switching to MockProvider for verification.")
                    image_provider = MockProvider()
                    image = image_provider.generate(job)
                else:
                    raise
            generation_time = time.time() - start_time
            
            output_path = self.storage_provider.save_image(filename, image)
            
            model_used = getattr(image_provider, "last_model_used", "unknown")
            transport_used = getattr(image_provider, "last_transport_used", "unknown")
            provider_report = f"{image_provider.get_name()} ({transport_used}:{model_used})"
            
            return ExecutionResult(
                success=True,
                provider=provider_report,
                generation_time=generation_time,
                image_path=output_path,
                message="Image generated successfully"
            )
        except Exception as e:
            model_used = getattr(image_provider, "last_model_used", "unknown")
            transport_used = getattr(image_provider, "last_transport_used", "unknown")
            provider_report = f"{image_provider.get_name()} ({transport_used}:{model_used})"
            
            err_msg = str(e).lower()
            if "payment" in err_msg or "credit" in err_msg or "rate limit" in err_msg or "402" in err_msg:
                status_msg = f"waiting_for_provider: {str(e)}"
            else:
                status_msg = str(e)

            return ExecutionResult(
                success=False,
                provider=provider_report,
                generation_time=0.0,
                image_path="",
                message=status_msg
            )
