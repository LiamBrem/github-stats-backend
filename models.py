from pydantic import BaseModel
from datetime import datetime

class PRMergedEvent(BaseModel):
    repo: str
    pr_number: int
    author: str
    additions: int
    deletions: int
    merged_at: datetime


class ReviewSubmittedEvent(BaseModel):
    repo: str
    pr_number: int
    reviewer: str
    review_state: str
    submitted_at: datetime
