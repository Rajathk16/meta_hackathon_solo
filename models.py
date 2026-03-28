from pydantic import BaseModel
from typing import List, Optional

class EmailPublic(BaseModel):
    id: str
    sender: str
    subject: str
    body: str
    timestamp: str

class Email(EmailPublic):
    expected_label: str

class Observation(BaseModel):
    inbox: List[EmailPublic]
    current_email: Optional[EmailPublic]
    steps: int

class Action(BaseModel):
    type: str
    email_id: str
    label: Optional[str] = None

class Reward(BaseModel):
    value: float
    reason: str