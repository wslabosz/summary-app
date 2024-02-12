# import logging
import time
from threading import Lock

from faster_whisper import WhisperModel

from .utils import load_audio

# logging.basicConfig()
# logging.getLogger("faster_whisper").setLevel(logging.DEBUG)
model = WhisperModel(
    model_size_or_path="tiny.en",
    device="cpu",
    compute_type="int8",
    cpu_threads=4,
)
model_lock = Lock()


def transcribe(
    audio,
):
    print("Transcribing audio...")
    start_time = time.time()
    with model_lock:
        segments = []
        text = ""
        segment_generator, info = model.transcribe(
            load_audio(audio),
            beam_size=1,
            vad_filter=True,
        )
        for segment in segment_generator:
            segments.append(segment)
            text = text + segment.text
        result = {
            "segments": segments,
            "text": text,
        }

    print(info.duration_after_vad, "seconds of audio after vad")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time} seconds")
    # return split_by_number_of_tokens(result["segments"], 3200)
    return result["text"]
