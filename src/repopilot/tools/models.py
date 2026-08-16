from pydantic import BaseModel
from typing import List


class PRRecommendation(BaseModel):
    rank: int
    title: str
    description: str
    impact: str
    difficulty: str
    estimated_time: str


class PRReport(BaseModel):
    recommendations: List[PRRecommendation]