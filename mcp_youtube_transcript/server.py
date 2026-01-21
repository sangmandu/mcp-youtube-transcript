import re
from mcp.server.fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)

mcp = FastMCP("youtube-transcript")


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


@mcp.tool()
def get_transcript(url: str, lang: str | None = None) -> str:
    """
    Get transcript from a YouTube video.

    Args:
        url: YouTube video URL or video ID
        lang: Language code (e.g., 'en', 'ko'). If not specified, uses the original language.

    Returns:
        Full transcript text
    """
    video_id = extract_video_id(url)
    api = YouTubeTranscriptApi()

    try:
        transcript_list = api.list(video_id)
        available_langs = [t.language_code for t in transcript_list]

        if lang:
            try:
                transcript = transcript_list.find_transcript([lang])
            except NoTranscriptFound:
                return f"Error: Language '{lang}' not available. Available: {', '.join(available_langs)}"
        else:
            try:
                transcript = transcript_list.find_manually_created_transcript(available_langs)
            except NoTranscriptFound:
                transcript = transcript_list.find_generated_transcript(available_langs)

        data = transcript.fetch()
        full_text = " ".join([entry.text for entry in data])

        return full_text

    except TranscriptsDisabled:
        return "Error: Transcripts are disabled for this video"
    except VideoUnavailable:
        return "Error: Video is unavailable"
    except NoTranscriptFound:
        return "Error: No transcripts found for this video"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_video_language(url: str) -> str:
    """
    Get the original language of a YouTube video.

    Args:
        url: YouTube video URL or video ID

    Returns:
        Original language information
    """
    video_id = extract_video_id(url)
    api = YouTubeTranscriptApi()

    try:
        transcript_list = api.list(video_id)

        generated = []
        manual = []

        for t in transcript_list:
            if t.is_generated:
                generated.append(f"{t.language_code} ({t.language})")
            else:
                manual.append(f"{t.language_code} ({t.language})")

        result = f"Video ID: {video_id}\n"
        if manual:
            result += f"Manual subtitles: {', '.join(manual)}\n"
        if generated:
            result += f"Original language: {', '.join(generated)}"

        return result

    except TranscriptsDisabled:
        return "Error: Transcripts are disabled for this video"
    except VideoUnavailable:
        return "Error: Video is unavailable"
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    mcp.run()


if __name__ == "__main__":
    main()
