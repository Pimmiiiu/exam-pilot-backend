from typing import List
from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: str
    email: str
    total_score: int


class LeaderboardResponse(BaseModel):
    entries: List[LeaderboardEntry]
