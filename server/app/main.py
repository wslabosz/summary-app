import os

from audio.download import download_audio
from fastapi import FastAPI
from firebase_admin import credentials, db, initialize_app, messaging
from pydantic import BaseModel
from speech_to_text.transcription import transcribe
from summarization.generate import summarize

from app.model.summary import store_summary
from app.model.transcript import store_transcript


def resolve_path(p):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), p))


app = FastAPI()
cred = credentials.Certificate(resolve_path("firebase.json"))
firebase_app = initialize_app(
    cred,
    {
        "databaseURL": "https://summaryai-fcdaa-default-rtdb.europe-west1.firebasedatabase.app/"
    },
)


class AudioRequest(BaseModel):
    video_id: str


class SummarizeRequest(BaseModel):
    video_title: str
    video_id: str
    transcription: str


@app.get("/")
def get_root():
    return {"hello": "world"}


@app.post("/audio")
def get_audio_file(req: AudioRequest):
    audio_buffer, video_title = download_audio(req.video_id)
    transcription = transcribe(audio_buffer)
    try:
        return store_transcript(
            req.video_id, "faster-whisper", transcription, video_title
        )
    except Exception as e:
        return {"error": e}


@app.post("/summarize")
def post_summarize(req: SummarizeRequest):
    summary_result = summarize(req.transcription)
    try:
        return store_summary(
            req.video_id,
            "mistral",
            summary_result["summary"],
            req.video_title,
            summary_result["system_prompt"],
        )
    except Exception as e:
        return {"error": e}


@app.get("/test")
def get_test():
    ref = db.reference("tokens").get()
    if ref is None:
        return {"tokens": []}
    tokens = list(ref.keys())
    for token in tokens:
        try:
            messaging.send(
                messaging.Message(
                    token=token,
                    webpush=messaging.WebpushConfig(
                        notification=messaging.WebpushNotification(
                            title="Hello",
                            body="World",
                        ),
                    ),
                )
            )
        except:
            pass

    return {"tokens": tokens}
