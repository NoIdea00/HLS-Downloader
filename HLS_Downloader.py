import os
import subprocess
import shutil
import requests
from tqdm import tqdm
import pyperclip

def set_console_encoding():
    """Set the console encoding to UTF-8 for Chinese input and output."""
    subprocess.run('chcp 65001', shell=True)

def reset_console_encoding():
    """Reset the console encoding to default after the script finishes."""
    subprocess.run('chcp 437', shell=True)  # Default for English-based systems

def read_lines_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def download_file(url, filename):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    total_size = int(r.headers.get('content-length', 0))
    with open(filename, 'wb') as f, tqdm(
        desc=f"Downloading {os.path.basename(filename)}",
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024
    ) as bar:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
            bar.update(len(chunk))
    print(f"[+] Downloaded: {filename}")

def process_m3u8(content, download_dir):
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        if line.startswith('#EXT-X-KEY'):
            start = line.find('URI="') + 5
            end = line.find('"', start)
            key_url = line[start:end]
            local_key_path = os.path.join(download_dir, 'key.key')
            download_file(key_url, local_key_path)
            line = line.replace(key_url, 'key.key')
        new_lines.append(line)
    return "\n".join(new_lines)

def check_line_counts(urls_file, names_file):
    urls = read_lines_from_file(urls_file)
    names = read_lines_from_file(names_file)
    if len(urls) != len(names):
        print(f"Error: {urls_file} has {len(urls)} lines.\n{names_file} has {len(names)} lines.")
        return urls, names, False
    return urls, names, True

def download_video(m3u8_url, folder_name, output_filename):
    os.makedirs(folder_name, exist_ok=True)
    playlist_path = os.path.join(folder_name, 'playlist.m3u8')
    output_path = os.path.join(folder_name, output_filename + '.mp4')

    print(f"\n[*] Downloading to folder: {folder_name}")
    r = requests.get(m3u8_url, stream=True)
    r.raise_for_status()
    content = r.text

    updated_playlist = process_m3u8(content, folder_name)

    with open(playlist_path, 'w', encoding='utf-8') as f:
        f.write(updated_playlist)

    print("[*] Running ffmpeg...")
    subprocess.run([
        'ffmpeg',
        '-protocol_whitelist', 'file,http,https,tcp,tls,crypto',
        '-allowed_extensions', 'ALL',
        '-i', playlist_path,
        '-c', 'copy',
        output_path
    ])

    print(f"[+] Download complete: {output_path}")
    return output_path

def move_all_downloads(video_paths):
    target_dir = "All Downloaded Videos"
    os.makedirs(target_dir, exist_ok=True)
    for video_path in video_paths:
        if os.path.exists(video_path):
            new_location = os.path.join(target_dir, os.path.basename(video_path))
            shutil.move(video_path, new_location)
            print(f"[→] Moved: {os.path.basename(video_path)}")

def batch_download():
    urls, names, valid = check_line_counts("m3u8_urls.txt", "video_names.txt")
    if not valid:
        return
    video_paths = []
    for i in range(len(urls)):
        folder_name = names[i]
        path = download_video(urls[i], folder_name, names[i])
        video_paths.append(path)

    move = input("Move all downloaded videos to 'All Downloaded Videos' folder? (y/n): ").strip().lower()
    if move == "y":
        move_all_downloads(video_paths)

def single_download():
    try:
        clipboard_url = pyperclip.paste().strip()
    except pyperclip.PyperclipException:
        clipboard_url = ""

    url = ""

    # If clipboard contains a valid URL
    if clipboard_url.startswith("http") and ".m3u8" in clipboard_url:
        print("[*] URL pasted from clipboard:")
        print(clipboard_url)
        use_clipboard = input("Use this URL? (y/n): ").strip().lower()
        if use_clipboard == "y":
            url = clipboard_url

    # Ask for URL if clipboard not used or invalid
    while not url:
        try:
            url_input = input("Enter the M3U8 video URL: ").strip()
        except EOFError:
            print("\n[!] Paste error or unexpected input. Try again.")
            continue

        if url_input.startswith("http") and ".m3u8" in url_input:
            url = url_input
        else:
            print("[!] Invalid URL. It must start with 'http' and contain '.m3u8'")

    # Ask for name (non-empty)
    while True:
        try:
            name = input("Enter the folder and video name: ").strip()
        except EOFError:
            print("\n[!] Input error. Try again.")
            continue

        if name:
            break
        else:
            print("[!] Name cannot be empty.")

    download_video(url, name, name)

def main():
    # Set console encoding to UTF-8 for Chinese input/output
    set_console_encoding()

    try:
        print("=== HLS Downloader ===")
        print("1. Batch Download (from m3u8_urls.txt and video_names.txt)")
        print("2. Single Video Download")
        print("0. Exit")

        choice = input("Choose an option (0-2): ").strip()
        if choice == "1":
            batch_download()
        elif choice == "2":
            single_download()
        elif choice == "0":
            print("Exiting...")
        else:
            print("Invalid option. Exiting...")
    finally:
        # Reset the console encoding back to default when the script finishes
        reset_console_encoding()

if __name__ == "__main__":
    main()
