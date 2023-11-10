from dataclasses import dataclass, field


@dataclass
class UserInfo:
    id: str
    name: str
    email: str
    password: str
    is_verified: bool = field(default=False)
