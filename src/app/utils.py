import re


def validate_yt_url(value):
    youtube_regex = (
        r"(?:https?://)?"
        r"(?:www\.)?"
        r"(?:youtube\.com/watch\?v=|youtu\.be/)"
        r"([a-zA-Z0-9_-]{11})"
    )

    pattern = re.compile(youtube_regex)
    return pattern.search(value) is not None


def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if match:
        return match.group(1)
    return None
