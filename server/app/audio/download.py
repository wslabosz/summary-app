import io

from pytube import Stream, YouTube


def download_audio(video_id: str) -> io.BytesIO:
    yt = YouTube(url=f"https://www.youtube.com/watch?v={video_id}")
    streams = yt.streams.filter(only_audio=True).order_by("abr").desc()
    stream_to_download: Stream = streams.last()
    if stream_to_download is None:
        raise Exception("No audio streams found")
    print(
        f"audio file size: {stream_to_download._filesize_mb}, format: {stream_to_download.subtype}"
    )
    file_buffer = io.BytesIO()
    stream_to_download.stream_to_buffer(buffer=file_buffer)
    return file_buffer, yt.title
