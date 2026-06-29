from dataclasses import dataclass
from typing import Optional

@dataclass
class GenerationJob:
    """Dataclass representing a Generation Job in the worker."""
    id: int
    scene_id: int
    shot_number: int
    provider: Optional[str]
    prompt: str
    negative_prompt: Optional[str]
    filename: Optional[str]
    status: str
    priority: int
    retry_count: int
    progress: int
    drive_file_id: Optional[str] = None
    generation_time: Optional[float] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "GenerationJob":
        """Instantiate GenerationJob from a dictionary representation."""
        return cls(
            id=data["id"],
            scene_id=data["scene_id"],
            shot_number=data["shot_number"],
            provider=data.get("provider"),
            prompt=data["prompt"],
            negative_prompt=data.get("negative_prompt"),
            filename=data.get("filename"),
            status=data["status"],
            priority=data.get("priority", 0),
            retry_count=data.get("retry_count", 0),
            progress=data.get("progress", 0),
            drive_file_id=data.get("drive_file_id"),
            generation_time=data.get("generation_time"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
