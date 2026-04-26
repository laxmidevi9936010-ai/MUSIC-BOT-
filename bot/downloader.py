import asyncio
import os
import re
import shutil
from pathlib import Path
from yt_dlp import YoutubeDL

DOWNLOAD_DIR = Path(os.getenv("DOWNLOAD_DIR", "downloads"))
DOWNLOAD_DIR.mkdir(exist_ok=True)

YDL_BASE = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "outtmpl": str(DOWNLOAD_DIR / "%(id)s.%(ext)s"),
    "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
}

def human_time(seconds):
    seconds = int(seconds or 0)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def is_spotify(url: str) -> bool:
    return "open.spotify.com" in url or url.startswith("spotify:")

async def spotify_to_audio(query: str):
    if not shutil.which("spotdl"):
        raise RuntimeError("Spotify ke liye spotdl install/available hona chahiye.")
    proc = await asyncio.create_subprocess_exec(
        "spotdl", "download", query, "--output", str(DOWNLOAD_DIR / "{title}.{output-ext}"),
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    _, err = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(err.decode()[-500:])
    newest = max(DOWNLOAD_DIR.glob("*.mp3"), key=lambda p: p.stat().st_mtime)
    return {"title": newest.stem, "duration": 0, "thumbnail": None, "file": str(newest), "webpage_url": query}

def ytdlp_download(query: str):
    search = query if re.match(r"https?://", query) else f"ytsearch1:{query}"
    with YoutubeDL(YDL_BASE) as ydl:
        info = ydl.extract_info(search, download=True)
        if "entries" in info:
            info = info["entries"][0]
        downloaded = Path(ydl.prepare_filename(info)).with_suffix(".mp3")
        return {
            "title": info.get("title", "Unknown Track"),
            "duration": info.get("duration") or 0,
            "thumbnail": info.get("thumbnail"),
            "file": str(downloaded),
            "webpage_url": info.get("webpage_url") or query,
        }

async def get_track(query: str):
    if is_spotify(query):
        return await spotify_to_audio(query)
    return await asyncio.to_thread(ytdlp_download, query)
