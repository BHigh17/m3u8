import time
import os
import requests
from tqdm import tqdm
import concurrent.futures
from threading import Lock

MAX_RETRIES = 3  # Number of times to retry downloading a segment
MAX_THREADS = os.cpu_count() * 3  # Number of threads for parallel downloading
print_lock = Lock()
console_lock = Lock()


def download_segment(segment_url, index):
    """Download a single segment with a retry mechanism."""
    for attempt in range(MAX_RETRIES):
        response = requests.get(segment_url, timeout=10, stream=True)
        if response.status_code == 200:
            return index, response.content, len(response.content)
        else:
            with print_lock, console_lock:
                print(f"\\nFailed to download {segment_url}. Attempt {attempt + 1} of {MAX_RETRIES}...")
            time.sleep(1.5)
    return index, None  # Failed to download after all retries


def download_segments(base_url, m3u8_content, output_file):
    """Download video segments in parallel and save them to the specified output file."""
    total_downloaded_size = 0
    ts_segments = [base_url + line for line in m3u8_content.splitlines() if line.endswith('.ts')]

    with open(output_file, 'wb') as f_out, concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for index, content, segment_size in tqdm(executor.map(download_segment, ts_segments, range(len(ts_segments))),
                                                 total=len(ts_segments), desc="Downloading", unit="segment", mininterval=0.05):
            if content:
                f_out.write(content)
                total_downloaded_size += segment_size
            else:
                with print_lock, console_lock:
                    print(f"\nFailed to download segment after {MAX_RETRIES} attempts.")
    return total_downloaded_size
