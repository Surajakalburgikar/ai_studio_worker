from dataclasses import dataclass

@dataclass
class ReporterConfig:
    """Configuration for the Reporter."""
    enabled: bool = True
