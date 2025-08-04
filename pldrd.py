import yt_dlp
import time
from tqdm import tqdm
import os

def download_video(url, output_template, retries=5):
    for attempt in range(retries):
        try:
            ydl_opts = {
                'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
                'merge_output_format': 'mp4',
                'outtmpl': output_template,
                'quiet': True,
                'noplaylist': True,
                'progress_hooks': [progress_hook],
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True

        except Exception as e:
            print(f"[!] Retry {attempt+1}/{retries} failed: {e}")
            time.sleep(2)

    print("[✗] Skipped after max retries.")
    return False

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0.0%').strip()
        tqdm.write(f"⏳ Downloading: {percent}", end="\r")
    elif d['status'] == 'finished':
        tqdm.write("✅ Finished downloading...")

def download_playlist(playlist_url):
    # Get metadata only first
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'force_generic_extractor': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

    playlist_title = info.get('title', 'playlist').strip().replace(" ", "_")
    videos = info.get('entries', [])
    total = len(videos)

    print(f"\n[🎵] Playlist: {playlist_title}")
    print(f"[🎬] Total Videos: {total}\n")

    os.makedirs(playlist_title, exist_ok=True)

    for i, video in enumerate(videos, start=1):
        if video is None or 'url' not in video:
            print(f"[!] Skipping item #{i}, missing data.")
            continue

        video_url = f"https://www.youtube.com/watch?v={video['id']}"
        title = video.get('title', f'video_{i}').replace("/", "_").strip()
        filename = f"{playlist_title}/{i:02d} - {title}.mp4"

        print(f"\n[{i}/{total}] 🎯 {title}")
        success = download_video(video_url, output_template=filename)

        if not success:
            with open("failed_downloads.txt", "a") as f:
                f.write(f"{video_url}\n")

    print("\n[✅] Playlist download complete.")
    print("Check `failed_downloads.txt` for skipped videos (if any).")

if __name__ == "__main__":
    url = input("Enter YouTube playlist URL: ").strip()
    download_playlist(url)

