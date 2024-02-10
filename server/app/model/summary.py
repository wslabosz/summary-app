from datetime import datetime

from firebase_admin import db
from pydantic import BaseModel


class StoreSummaryError(Exception):
    pass


class Summary(BaseModel):
    date_created: datetime = datetime.now()
    system_prompt: str
    summary: str
    model: str
    video_title: str


def store_summary(
    video_id: str, model: str, summary: str, video_title: str, system_prompt: str
) -> dict[str, datetime | str]:
    try:
        record = Summary(
            system_prompt=system_prompt,
            summary=summary,
            model=model,
            video_title=video_title,
        ).model_dump(mode="json")
        ref = db.reference(f"summaries/{video_id}")
        ref.set(record)
        return record
    except Exception as e:
        raise StoreSummaryError(f"{e}: during store_summary")
