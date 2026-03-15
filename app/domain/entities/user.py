from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class UserEntity:
    id: str
    email: str
    password_hash: str
    role: str
    created_at: datetime
    is_active: bool = True
