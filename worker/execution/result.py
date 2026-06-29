from dataclasses import dataclass

@dataclass
class ExecutionResult:
    """Represents the outcome of a job execution."""
    success: bool
    provider: str
    generation_time: float
    image_path: str
    message: str
