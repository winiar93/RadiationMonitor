from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class GeigerReading(BaseModel):
    cpm: int = Field(..., ge=0, description="Counts per minute (must be >= 0)")
    usvh: float = Field(..., ge=0, description="Counts per second (must be >= 0)")
    timestamp: Optional[datetime] = Field(
        default=None,
        description="UTC timestamp, auto-generated if not provided"
    )

    def ensure_timestamp(self):
        """Uzupełnia timestamp jeśli nie został podany"""
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
        return self