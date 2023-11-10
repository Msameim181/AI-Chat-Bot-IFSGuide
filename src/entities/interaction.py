from dataclasses import dataclass, field
from datetime import datetime, timezone


def current_time():
    return datetime.now(timezone.utc)


def settings():
    return {
        "model_name": "gpt-4",
        "role": "System",
        "prompt": "As a helpful IFS therapist chatbot, your role is to guide users through a "
        "simulated IFS session in a safe and supportive manner with a few changes to the exact steps of the IFS model.",
    }


@dataclass
class Interaction:
    id: str
    user_id: str
    settings: dict = field(default_factory=settings)
    created_at: datetime = field(default_factory=current_time)
    updated_at: datetime = field(default_factory=current_time)
