# 🔹 HLS Video Downloader Script

This script allows you to **download and decrypt HLS (.m3u8) video streams** by processing `.m3u8` playlist URLs. It handles encrypted streams, downloads video segments, and merges them into MP4 files using FFmpeg.

---

## 📦 Features

- Batch download from multiple `.m3u8` URLs
- Auto-download and inject encryption keys (if present)
- Merge segments into `.mp4` using FFmpeg
- Auto-numbered folders (`video_1`, `video_2`, etc.) — avoids overwriting

---

## 🛠 Prerequisites

### 1. Python 3.x
- Required to run the script.
- [Download Python](https://www.python.org/downloads/)
```bash
python --version
```

### 2. Python Libraries
- `requests` is used to fetch remote files.
```bash
pip install requests
```

### 3. FFmpeg
- Used to merge `.ts` segments into a final `.mp4`.
- [Download FFmpeg](https://ffmpeg.org/download.html) and **add it to your system PATH**.

Check FFmpeg installation:
```bash
ffmpeg -version
```

---

## 📂 File Setup

### 1. `m3u8_urls.txt`
- Create this file in the same directory as the script.
- Add one `.m3u8` URL per line:
```
https://example.com/video1.m3u8?auth_key=abc123
https://example.com/video2.m3u8?auth_key=xyz456
```

### 2. Python Script
- The script will read URLs, download segments and keys (if any), and convert them into `.mp4`.

---

## ▶️ How to Use

1. Place `.m3u8` URLs inside `m3u8_urls.txt`.
2. Run the script:
```bash
python your_script.py
```
3. Output:
   - A folder will be created per URL (`video_1`, `video_2`, etc.)
   - Each folder contains:
     - `playlist.m3u8`
     - `key.key` (if encrypted)
     - `output.mp4` (final video)

---

## 🧠 How It Works

- **Reads** all URLs from `m3u8_urls.txt`
- **Downloads** and rewrites playlists to use local key paths
- **Decrypts** using `key.key` if needed
- **Combines** `.ts` segments into a final `.mp4` using FFmpeg

---

## ❓ How to Get `.m3u8` Links

### 🔍 Method 1: Network Tab (Browser)
1. Open the video in your browser.
2. Press `F12` to open Developer Tools → Go to **Network** tab.
3. Filter by `m3u8` and reload/play the video.
4. Right-click on the `.m3u8` URL → **Copy link address**

### 🎥 Bonus: If Only `.ts` Files Appear
- View page source (`Ctrl+U`) and search for `.m3u8`
- Inspect JavaScript files that load video dynamically

---

## ❗ Troubleshooting

| Problem                    | Solution                                                  |
|---------------------------|-----------------------------------------------------------|
| `ffmpeg` not found        | Ensure it's installed and added to PATH                  |
| `requests` not installed  | Run `pip install requests`                                |
| Download fails            | Check if URL is still valid and publicly accessible       |

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## 💡 Contributions

Feel free to fork and enhance this script! PRs are welcome.