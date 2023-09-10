import os
import requests
from threading import Lock
from components.helper import *
from components.ts_download import download_segments

directory = 'downloadedVideos'
if not os.path.exists(directory):
    os.makedirs(directory)

MAX_THREADS = os.cpu_count() * 3  # Number of threads for parallel downloading
print_lock = Lock()
DEBUG = False  # Set to True for non-debug builds
console_lock = Lock()


def main():
    M3U8_URL = 'https://di2g5yar1p6ph.cloudfront.net/3bkyqwhv/1080p30-3.0.hls/index.m3u8' \
        if DEBUG else input(
        "Please enter the M3U8 URL index.u3m8 playlist: ")
    user_filename = 'debugtestfile' \
        if DEBUG else input(
        "Enter the desired name for the output file (without extension): ")

    base_url = get_base_url(M3U8_URL)
    processed_filename = os.path.join(directory, camel_case_filename(user_filename) + ".ts")

    response = requests.get(M3U8_URL, timeout=10)
    if response.status_code == 200:
        m3u8_content = response.text
        total_segments = len([line for line in m3u8_content.splitlines() if line.endswith('.ts')])

        with print_lock, console_lock:
            print(f"Max number of threads to be used: {MAX_THREADS}")
            print(f"Number of segments to be downloaded: {total_segments}")
            print(f"Using {MAX_THREADS} threads for downloading.")

        total_downloaded_size = download_segments(base_url, m3u8_content, processed_filename)

        with print_lock, console_lock:
            print(f"\\nDownload completed. Check {processed_filename}")
            print(f'\nTotal downloaded size: {format_size(total_downloaded_size)}')
    else:
        with print_lock, console_lock:
            print(f"Failed to fetch the M3U8 playlist from {M3U8_URL}")


if __name__ == "__main__":
    main()
