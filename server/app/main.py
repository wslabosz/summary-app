import os

from app.model.summary import retrieve_summary, store_summary
from app.model.transcript import retrieve_transcript, store_transcript
from app.summarization.config import get_model_list
from audio.download import download_audio
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials, initialize_app
from pydantic import BaseModel
from speech_to_text.transcription import transcribe
from summarization.generate import summarize

load_dotenv()


def resolve_path(p):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), p))


cred = credentials.Certificate(resolve_path("firebase.json"))
app = FastAPI(
    ssl_keyfile="certs/localhost-key.pem",
    ssl_certfile="certs/localhost-cert.pem",
)
origins = [
    "https://localhost:5173",
    "https://localhost:5678",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
router = APIRouter()
firebase_app = initialize_app(
    cred,
    {
        "databaseURL": "https://summaryai-fcdaa-default-rtdb.europe-west1.firebasedatabase.app/"
    },
)


class SummarizeRequest(BaseModel):
    video_title: str
    video_id: str
    transcription: str
    model: str


@router.get("/")
def get_root():
    return {"hello": "world"}


@router.get("/models", status_code=status.HTTP_200_OK)
def get_models():
    return {"models": list(get_model_list())}


@router.get("/summary/{video_id}/{model}", status_code=status.HTTP_200_OK)
def get_summary(video_id: str, model: str | None):
    summary = retrieve_summary(video_id=video_id, model=model)
    if summary is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found"
        )
    return summary


@router.get("/transcription/{video_id}", status_code=status.HTTP_200_OK)
def get_transcription(video_id: str):
    transcription = retrieve_transcript(video_id=video_id)
    if transcription is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transcription not found"
        )
    return transcription


@router.post("/transcription/{video_id}", status_code=status.HTTP_201_CREATED)
def post_transcribe(video_id: str):
    audio_buffer, video_title = download_audio(video_id)
    transcription = transcribe(audio_buffer)
    try:
        return store_transcript(video_id, "faster-whisper", transcription, video_title)
    except Exception as e:
        # TODO: work on error handling
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {e} during store_transcript",
        )


@router.post("/summarize", status_code=status.HTTP_201_CREATED)
def post_summarize(req: SummarizeRequest):
    summary_result = summarize(req.transcription, req.model)
    try:
        return store_summary(
            req.video_id,
            req.model,
            summary_result["summary"],
            req.video_title,
            summary_result["system_prompt"],
        )
    except Exception as e:
        # TODO: work on error handling
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {e} during store_summary",
        )


app.include_router(router)
