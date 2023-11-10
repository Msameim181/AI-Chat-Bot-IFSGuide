from dataclasses import dataclass, field
from datetime import datetime, timezone

def current_time():
    return datetime.now(timezone.utc)

@dataclass
class User:
    id: str
    name: str
    email: str
    password: str
    is_verified: bool = field(default=False)
    created_at: datetime = field(default_factory=current_time)
    updated_at: datetime = field(default_factory=current_time)
