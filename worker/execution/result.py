from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class ExecutionResult:
    """Represents the outcome of a job execution."""
    status: str
    provider: str
    filename: str
    output_path: str
    generation_time: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
