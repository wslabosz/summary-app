from io import BytesIO

import ffmpeg
import numpy as np


def load_audio(bytes_stream: BytesIO, sr: int = 16000):
    """
    Open an audio file and read as mono waveform, resampling as necessary

    Parameters
    ----------
    bytes_stream: BytesIO
        Bytes stream of audio file

    sr: int
        The sample rate to resample the audio if necessary

    Returns
    -------
    A NumPy array containing the audio waveform, in float32 dtype.
    """

    try:
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        out, _ = (
            ffmpeg.input("pipe:", threads=0)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
            .run(
                cmd="ffmpeg",
                capture_stdout=True,
                capture_stderr=True,
                input=bytes_stream.getvalue(),
            )
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0


def split_by_number_of_tokens(segments: list[dict], number_of_tokens: int) -> list[str]:
    if not segments:
        return []

    splitted_text = []
    current_fragment = []
    current_tokens = 0

    for segment_info in segments:
        current_fragment.append(segment_info["text"])
        current_tokens += len(segment_info["tokens"])

        if current_tokens > number_of_tokens:
            splitted_text.append("".join(current_fragment))
            current_fragment = []
            current_tokens = 0

    # Handle the last segment if it exceeds the limit
    if current_fragment:
        splitted_text.append("".join(current_fragment))

    return splitted_text
