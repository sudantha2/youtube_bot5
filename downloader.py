import yt_dlp
import os
import uuid

def download_video(url, format_code):
    filename = f"{uuid.uuid4().hex}"

    ydl_opts = {
        'outtmpl': f'downloads/{filename}.%(ext)s',
        'quiet': True,
    }

    if format_code.startswith("mp3"):
        bitrate = format_code.replace("mp3", "")
        ydl_opts.update({
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate
            }]
        })
    else:
        ydl_opts['format'] = f'bestvideo[height<={format_code}]+bestaudio/best'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        ext = 'mp3' if format_code.startswith("mp3") else info.get("ext", "mp4")
        return f"downloads/{filename}.{ext}"
