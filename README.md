# MCP YouTube Transcript

MCP server for fetching YouTube video transcripts.

## Features

- **get_transcript**: Get full transcript text from a YouTube video
- **get_video_language**: Detect the original language of a YouTube video

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (Python package manager)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/sangmandu/mcp-youtube-transcript.git
cd mcp-youtube-transcript
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure Claude Desktop

Open your Claude Desktop config file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the following to `mcpServers`:

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "/path/to/uv",
      "args": [
        "--directory",
        "/path/to/mcp-youtube-transcript",
        "run",
        "python",
        "-m",
        "mcp_youtube_transcript.server"
      ]
    }
  }
}
```

> **Note**: Replace `/path/to/uv` with the actual path to uv (run `which uv` to find it), and `/path/to/mcp-youtube-transcript` with the actual path to the cloned repository.

### 4. Restart Claude Desktop

Quit Claude Desktop completely (Cmd+Q on macOS) and reopen it.

## Usage

Once configured, you can use the following tools in Claude Desktop:

### get_transcript

Get the full transcript of a YouTube video.

```
get_transcript(url="https://www.youtube.com/watch?v=VIDEO_ID", lang="en")
```

- `url`: YouTube video URL or video ID
- `lang` (optional): Language code (e.g., 'en', 'ko'). If not specified, uses the original language.

### get_video_language

Detect the original language of a YouTube video.

```
get_video_language(url="https://www.youtube.com/watch?v=VIDEO_ID")
```

## References

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [MCP Quickstart Guide](https://modelcontextprotocol.io/docs/quickstart)
- [Claude Desktop](https://claude.ai/download)
- [uv - Python Package Manager](https://docs.astral.sh/uv/)

## License

MIT
