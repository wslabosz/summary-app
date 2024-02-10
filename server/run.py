import sys

from app.audio.download import download_audio
from app.speech_to_text.transcription import transcribe
from app.summarization.generate import summarize

# https://www.youtube.com/watch?v=4ORZ1GmjaMc - reactjs state
# https://www.youtube.com/watch?v=TNhaISOUy6Q - react hooks
# https://www.youtube.com/watch?v=hQAHSlTtcmY - react 30 minute tutorial
# https://www.youtube.com/watch?v=SqrbIlUwR0U - golang 1:38 tutorial
url = "https://www.youtube.com/watch?v=TNhaISOUy6Q"


if __name__ == "__main__":
    print("Downloading audio...")
    if sys.argv[1]:
        url = sys.argv[1]
    bytes, _ = download_audio(url)
    print("Generating summary...")
    transcription = transcribe(bytes)
    # with open(
    #     os.path.abspath(
    #         os.path.join(
    #             os.path.dirname(__file__),
    #             "summaries/10 React Hooks Explained  Plus Build your own from Scratch/transcription.txt",
    #         )
    #     )
    # ) as f:
    #     transcription = f.read()
    print(summarize(transcription))
