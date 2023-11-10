from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


def current_time():
    return datetime.now(timezone.utc)


class RoleType(Enum):
    HUMAN = "human"
    AI = "ai"


@dataclass
class Message:
    id: str
    interaction_id: str
    role: RoleType
    content: str
    created_at: datetime = field(default_factory=current_time)
    updated_at: datetime = field(default_factory=current_time)
