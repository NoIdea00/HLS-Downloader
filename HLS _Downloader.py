import requests
import os
import subprocess

# Read URLs from m3u8_urls.txt
def read_urls_from_file(filename="m3u8_urls.txt"):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def download_file(url, filename):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
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

def get_unique_folder_name(base_name):
    """Generate a unique folder name by checking existing folders"""
    i = 1
    while os.path.exists(f"{base_name}_{i}"):
        i += 1
    return f"{base_name}_{i}"

def download_video(m3u8_url, index):
    folder_name = get_unique_folder_name("video")
    os.makedirs(folder_name, exist_ok=True)
    playlist_path = os.path.join(folder_name, 'playlist.m3u8')
    output_path = os.path.join(folder_name, 'output.mp4')

    print(f"\n[*] Downloading playlist {index} to folder {folder_name}...")
    r = requests.get(m3u8_url)
    r.raise_for_status()
    playlist_content = r.text

    print("[*] Processing playlist...")
    updated_playlist = process_m3u8(playlist_content, folder_name)

    with open(playlist_path, 'w') as f:
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

def main():
    urls = read_urls_from_file("m3u8_urls.txt")
    for i, url in enumerate(urls, start=1):
        download_video(url, i)

if __name__ == "__main__":
    main()
