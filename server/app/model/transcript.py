from datetime import datetime

from firebase_admin import db
from pydantic import BaseModel


class StoreTranscriptError(Exception):
    pass


class Transcript(BaseModel):
    date_created: datetime = datetime.now()
    transcription: str
    video_title: str


def store_transcript(
    video_id: str, model: str, transcription: str, video_title: str
) -> dict[str, datetime | str]:
    try:
        record = Transcript(
            transcription=transcription,
            video_title=video_title,
        ).model_dump(mode="json")
        ref = db.reference(f"transcripts/{video_id}/{model}")
        ref.set(record)
        record.update({"video_id": video_id, "model": model})
        return record
    except Exception as e:
        raise StoreTranscriptError(f"{e}: during store_transcript")


def retrieve_transcript(
    video_id: str, model: str | None = "faster-whisper"
) -> dict[str, datetime | str]:
    return db.reference(f"transcripts/{video_id}/{model}").get()
