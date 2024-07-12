import re

def validate_yt_url(value):
    youtube_regex = (
        r'(?:https?://)?'
        r'(?:www\.)?'
        r'(?:youtube\.com/watch\?v=|youtu\.be/)'
        r'([a-zA-Z0-9_-]{11})'
    )

    pattern = re.compile(youtube_regex)
    return pattern.search(value) is not None
