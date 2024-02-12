from datetime import datetime

from firebase_admin import db
from pydantic import BaseModel


class StoreSummaryError(Exception):
    pass


class Summary(BaseModel):
    date_created: datetime = datetime.now()
    system_prompt: str
    summary: str
    video_title: str


def store_summary(
    video_id: str, model: str, summary: str, video_title: str, system_prompt: str
) -> dict[str, datetime | str]:
    try:
        record = Summary(
            system_prompt=system_prompt,
            summary=summary,
            video_title=video_title,
        ).model_dump(mode="json")
        ref = db.reference(f"summaries/{video_id}/{model}")
        ref.set(record)
        return record
    except Exception as e:
        raise StoreSummaryError(f"{e}: during store_summary")


def retrieve_summary(
    video_id: str, model: str | None
) -> dict[str, datetime | str] | None:
    if model is None:
        model = "mistral"
    record = db.reference(f"summaries/{video_id}/{model}").get()
    if record is None:
        return None
    else:
        return {
            "dateCreated": record["date_created"],
            "summary": record["summary"],
            "videoTitle": record["video_title"],
            "videoId": video_id,
            "model": model,
        }
