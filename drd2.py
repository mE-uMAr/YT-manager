import yt_dlp
import os

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
        'progress_hooks': [progress_hook],
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', 'video')
        print(f"[+] Title: {title}")
        formats = info_dict.get('formats', [])
        list_formats(formats)
        choice = int(input("Enter the number of the format to download: "))
        ydl.params['format'] = formats[choice]['format_id']
        ydl.download([url])

def list_formats(formats):
    print("\nAvailable formats:\n")
    for i, fmt in enumerate(formats):
        if fmt.get('vcodec') != 'none' and fmt.get('acodec') == 'none':
            res = fmt.get('format_note', fmt.get('height', 'N/A'))
            ext = fmt.get('ext', '')
            size = fmt.get('filesize_approx', fmt.get('filesize', 0))
            size_mb = round(size / (1024*1024), 2) if size else 'Unknown'
            print(f"[{i}] {res} | {fmt['format_id']} | {ext.upper()} | {size_mb} MB")

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"\rDownloading: {d['_percent_str']} ETA: {d.get('eta', '?')}s", end='')
    elif d['status'] == 'finished':
        print(f"\n[✓] Done downloading, now merging...")

if __name__ == "__main__":
    url = input("Enter YouTube video URL: ").strip()
    if "?" in url:
        url = url.split("?")[0]
    download_video(url)

