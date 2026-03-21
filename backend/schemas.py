from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class LogBase(BaseModel):
    source_ip: str
    destination_ip: str
    protocol: str
    bytes_transferred: int
    event_type: str
    details: Optional[str] = None


class LogCreate(LogBase):
    pass


class LogResponse(LogBase):
    id: int
    timestamp: datetime

    # Pydantic v2: use model_config instead of inner class Config
    model_config = ConfigDict(from_attributes=True)


class PredictionRequest(LogBase):
    pass


class PredictionResponse(BaseModel):
    is_anomaly: bool
    anomaly_score: float
