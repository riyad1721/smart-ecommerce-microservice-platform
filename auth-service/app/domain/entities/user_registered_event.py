from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserRegisteredEvent:
    event_type: str
    user_id: UUID
    email: str
    full_name: str
    occurred_at: datetime