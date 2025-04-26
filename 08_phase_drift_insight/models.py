from pydantic import BaseModel

class PhaseState(BaseModel):
    phase_name: str
    drift_value: float
    timestamp: str
    additional_info: dict

class Feedback(BaseModel):
    feedback_type: str
    details: str
    timestamp: str
