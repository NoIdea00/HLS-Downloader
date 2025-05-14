# 🔹 HLS Video Downloader Script

This Python script provides a convenient way to download videos from `.m3u8` HLS stream URLs. It supports:

- **Single video downloads** via URL input or clipboard.
- **Batch downloads** using two text files (`m3u8_urls.txt` and `video_names.txt`).
- Automatic key downloading and playlist rewriting for encrypted streams.
- Merging video segments into a single `.mp4` using `ffmpeg`.
- Organizing all completed downloads into a centralized folder.

---

## 📦 Features

- ✅ Batch and single download support
- ✅ Clipboard URL detection (auto-paste)
- ✅ Encrypted `.m3u8` support
- ✅ Download progress bar with `tqdm`
- ✅ Automatically moves final videos into "All Downloaded Videos" (optional)
- ✅ UTF-8 console encoding for multilingual support (e.g. Chinese)

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
### 4.tqdm
```bash
pip install requests tqdm 
```
### 5.pyperclip
```bash
pip install requests pyperclip
```

---

## 📂 File Setup

project_folder/
│
├── downloader.py            # Main script
├── m3u8_urls.txt            # List of .m3u8 URLs (one per line)
├── video_names.txt          # Corresponding video names (one per line)
├── All Downloaded Videos/   # (Created automatically)
└── README.md

### 1. `m3u8_urls.txt`
- Create this file in the same directory as the script.
- Add one `.m3u8` URL per line:
```
https://example.com/video1.m3u8?auth_key=abc123
https://example.com/video2.m3u8?auth_key=xyz456
```

### 2. Python Script
- The script will read URLs, download segments and keys (if any), and convert them into `.mp4`.

### 3. `video_names.txt`
- Create this file in the same directory as the script.
- Add one `video name` URL per line:
```
crazyfox
appleorange
yellowblue
```

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

- Reads all URLs from m3u8_urls.txt
- Downloads and rewrites playlists to use local key paths
- Decrypts using key.key if needed
- Combines .ts segments into a final .mp4 using FFmpeg
- Handles both single and batch download modes
- Automatically prompts for URL if clipboard is empty or invalid
- Validates matching line count between URL and name files before processing
- Moves all finished videos to a central directory if user agrees


---

You will see:

```
=== HLS Downloader ===
1. Batch Download (from m3u8_urls.txt and video_names.txt)
2. Single Video Download
0. Exit
```

### 🧩 Batch Download Mode

Prepare the following files in the same directory:

- `m3u8_urls.txt` – list of `.m3u8` links
- `video_names.txt` – desired output folder/video names (matching line count)

Then run the script and choose **option 1**.

### 📥 Single Download Mode

Choose **option 2**, then either:

- Let it auto-read from clipboard
- Paste a `.m3u8` URL manually
- Provide a name for the folder/video


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

No Thanks!
