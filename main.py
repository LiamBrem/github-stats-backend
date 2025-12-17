import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Header
from db import get_connection
from models import PRMergedEvent, ReviewSubmittedEvent
app = FastAPI()

API_KEY = os.environ["LEADERBOARD_API_KEY"]


def verify_auth(auth: str | None):
    if auth != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="unauthorized")


@app.post("/events/pr-merged")
def pr_merged(
    event: PRMergedEvent,
    authorization: str | None = Header(default=None),
):
    verify_auth(authorization)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                insert into pr_events
                  (repo, pr_number, author, additions, deletions, merged_at)
                values
                  (%s, %s, %s, %s, %s, %s)
                """,
                (
                    event.repo,
                    event.pr_number,
                    event.author,
                    event.additions,
                    event.deletions,
                    event.merged_at,
                ),
            )

    return {"status": "ok"}


@app.post("/events/review-submitted")
def review_submitted(
    event: ReviewSubmittedEvent,
    authorization: str | None = Header(default=None),
):
    verify_auth(authorization)

    if event.review_state == "commented":
        return {"status": "ignored"}

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                insert into review_events
                  (repo, pr_number, reviewer, review_state, submitted_at)
                values
                  (%s, %s, %s, %s, %s)
                """,
                (
                    event.repo,
                    event.pr_number,
                    event.reviewer,
                    event.review_state,
                    event.submitted_at,
                ),
            )

    return {"status": "ok"}

