import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)


def extract_video_id(url_or_id: str) -> str:
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id

    patterns = [
        r'(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})',
        r'(?:youtu\.be\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/v\/)([a-zA-Z0-9_-]{11})',
    ]

    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)

    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def get_transcript(url_or_id: str, lang: str | None = None) -> dict:
    video_id = extract_video_id(url_or_id)
    api = YouTubeTranscriptApi()

    try:
        transcript_list = api.list(video_id)
        available_langs = [t.language_code for t in transcript_list]

        if lang:
            try:
                transcript = transcript_list.find_transcript([lang])
            except NoTranscriptFound:
                return {
                    "success": False,
                    "error": f"Language '{lang}' not available. Available: {', '.join(available_langs)}",
                    "available_languages": available_langs,
                }
        else:
            try:
                transcript = transcript_list.find_manually_created_transcript(available_langs)
            except NoTranscriptFound:
                transcript = transcript_list.find_generated_transcript(available_langs)

        data = transcript.fetch()

        full_text = " ".join([entry.text for entry in data])

        return {
            "success": True,
            "video_id": video_id,
            "language": transcript.language_code,
            "is_generated": transcript.is_generated,
            "segments": [{"text": s.text, "start": s.start, "duration": s.duration} for s in data],
            "full_text": full_text,
            "available_languages": available_langs,
        }

    except TranscriptsDisabled:
        return {
            "success": False,
            "error": "Transcripts are disabled for this video",
        }
    except VideoUnavailable:
        return {
            "success": False,
            "error": "Video is unavailable",
        }
    except NoTranscriptFound:
        return {
            "success": False,
            "error": "No transcripts found for this video",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
