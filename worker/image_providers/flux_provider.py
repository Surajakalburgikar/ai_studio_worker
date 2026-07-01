"""
FLUX Image Provider — Real AI image generation via Hugging Face Inference API.

This provider is responsible ONLY for:
    - Reading configuration
    - Authenticating with Hugging Face
    - Generating an image
    - Returning the generated image as a PIL Image

This provider MUST NOT:
    - Save images
    - Talk to the backend
    - Update jobs
    - Report progress
    - Know about storage, queue, reporter, or executor
"""

from PIL import Image
from huggingface_hub import InferenceClient
from worker.config import settings
from worker.models.job import GenerationJob
from .base import BaseImageProvider


class FluxProvider(BaseImageProvider):
    """Real FLUX image provider using Hugging Face Inference API.

    All Hugging Face implementation details are isolated inside this class.
    Future replacements (RunPod, ComfyUI, Local SDXL) require changes
    only inside this provider, not in Executor, Storage, or Reporter.
    """

    def __init__(self) -> None:
        self._validate_config()
        self.client = self._create_client()
        print(f"[Flux] Provider loaded — model={settings.hf_model}, "
              f"provider={settings.hf_provider}, timeout={settings.hf_timeout}s")

    def get_name(self) -> str:
        """Return the name of this image provider."""
        return "flux"

    def generate(self, job: GenerationJob) -> Image.Image:
        """Generate a real AI image from the job prompt.

        Args:
            job: GenerationJob containing prompt and optional negative_prompt.

        Returns:
            PIL.Image.Image — the generated image.
        """
        prompt = job.prompt
        negative_prompt = job.negative_prompt

        spec = getattr(job, "generation_spec", None) if job else None

        # Determine model
        model = settings.hf_model
        if spec and spec.get("model"):
            model = spec.get("model")

        # Determine provider transport dynamically
        provider_transport = None
        if spec and spec.get("provider"):
            provider_transport = spec.get("provider")
        if not provider_transport:
            provider_transport = settings.hf_provider
            
        if provider_transport == "flux":
            provider_transport = None

        print(f"[Flux] Generating image for job {job.id}")
        print(f"[Flux] Model: {model}, Transport: {provider_transport or 'serverless'}")
        print(f"[Flux] Prompt: {prompt[:100]}")

        if negative_prompt:
            print(f"[Flux] Negative prompt: {negative_prompt[:80]}")

        # Build dynamic client
        if provider_transport:
            client = InferenceClient(
                provider=provider_transport,
                api_key=settings.hf_token,
            )
        else:
            client = InferenceClient(
                api_key=settings.hf_token,
            )

        kwargs = self._build_request_kwargs(prompt, negative_prompt, job=job)
        self.last_model_used = model
        self.last_transport_used = provider_transport or "serverless"

        try:
            print("[Flux] Sending request to Hugging Face...")
            image = client.text_to_image(**kwargs)
            print("[Flux] Image generated successfully")
            return image
        except Exception as e:
            # 1. Same-model transport fallback (always allowed)
            if provider_transport:
                print(f"[Flux] Transport {provider_transport} failed: {e}. Attempting same-model transport fallback to serverless...")
                try:
                    fallback_client = InferenceClient(api_key=settings.hf_token)
                    image = fallback_client.text_to_image(**kwargs)
                    self.last_transport_used = "serverless"
                    print("[Flux] Image generated successfully via fallback transport")
                    return image
                except Exception as fe:
                    print(f"[Flux] Fallback transport failed: {fe}")

            # 2. Quality-downgrade fallback (if enabled in metadata)
            quality_mode = "production"
            allow_downgrade = False
            if spec and spec.get("metadata"):
                quality_mode = spec["metadata"].get("quality_mode", "production")
                allow_downgrade = spec["metadata"].get("allow_quality_downgrade", False)

            if quality_mode != "production" and allow_downgrade:
                if "dev" in model.lower():
                    schnell_model = "black-forest-labs/FLUX.1-schnell"
                    print(f"[Flux] Quality policy permits downgrade. Attempting fallback to {schnell_model}...")
                    try:
                        kwargs["model"] = schnell_model
                        fallback_client = InferenceClient(api_key=settings.hf_token)
                        image = fallback_client.text_to_image(**kwargs)
                        self.last_model_used = schnell_model
                        self.last_transport_used = "serverless"
                        print(f"[Flux] Image generated successfully via fallback model {schnell_model}")
                        return image
                    except Exception as fe:
                        print(f"[Flux] Fallback model failed: {fe}")

            raise self._classify_error(e) from e

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _validate_config(self) -> None:
        """Validate that required Hugging Face configuration is present."""
        if not settings.hf_token:
            raise ValueError(
                "[Flux] HF_TOKEN is not set. "
                "Please set HF_TOKEN in your .env file."
            )

    def _create_client(self) -> InferenceClient:
        """Create and return a configured Hugging Face InferenceClient."""
        print("[Flux] Loading provider...")
        if settings.hf_provider:
            return InferenceClient(
                provider=settings.hf_provider,
                api_key=settings.hf_token,
            )
        else:
            return InferenceClient(
                api_key=settings.hf_token,
            )

    def _build_request_kwargs(self, prompt: str, negative_prompt: str | None, job: GenerationJob = None) -> dict:
        """Build the keyword arguments dictionary for the text_to_image call."""
        model = settings.hf_model
        
        spec = getattr(job, "generation_spec", None) if job else None
        if spec and spec.get("model"):
            model_val = spec.get("model")
            if "/" in model_val:
                model = model_val

        kwargs: dict = {
            "prompt": prompt,
            "model": model,
        }

        if negative_prompt:
            kwargs["negative_prompt"] = negative_prompt

        if spec:
            gen_params = spec.get("generation_parameters", {})
            if gen_params.get("width"):
                kwargs["width"] = gen_params.get("width")
            if gen_params.get("height"):
                kwargs["height"] = gen_params.get("height")
            if gen_params.get("steps"):
                kwargs["num_inference_steps"] = gen_params.get("steps")
            if gen_params.get("guidance_scale"):
                kwargs["guidance_scale"] = gen_params.get("guidance_scale")
            if gen_params.get("seed") is not None:
                kwargs["seed"] = gen_params.get("seed")

        return kwargs

    def _classify_error(self, error: Exception) -> Exception:
        """Classify a raw exception into a meaningful provider error.

        This keeps error semantics clean for the Executor and Reporter
        without leaking Hugging Face-specific exception types.
        """
        error_msg = str(error).lower()

        if "401" in error_msg or "403" in error_msg or "unauthorized" in error_msg:
            print(f"[Flux] Authentication error: {error}")
            return PermissionError(f"[Flux] Authentication failed: {error}")

        if "timeout" in error_msg or "timed out" in error_msg:
            print(f"[Flux] Timeout error: {error}")
            return TimeoutError(f"[Flux] Request timed out: {error}")

        if "connection" in error_msg or "network" in error_msg:
            print(f"[Flux] Network error: {error}")
            return ConnectionError(f"[Flux] Network failure: {error}")

        # Catch-all for provider errors, rate limits, bad requests, etc.
        print(f"[Flux] Provider error: {error}")
        return RuntimeError(f"[Flux] Generation failed: {error}")
