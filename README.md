# Media Downloader by Yash

<p align="center">
  <img src="./assets/logo.png" width="180" alt="Media Downloader Logo">
  <br>
  <b>**Media Downloader Pro** is a high-performance, professional-grade media extraction tool designed for power users who demand the highest quality content. Unlike standard downloaders that limit you to 360p or low-bitrate audio, this app unlocks the full potential of your media links, allowing for seamless extraction of **4K and 8K Ultra-HD video** and high-fidelity **320kbps audio**.

  Powered by a sharded parallel download engine and integrated with FFmpeg for precise trimming, it serves as a centralized hub for archiving content from over **1,000+ websites** with zero quality loss.
</b>
</p>

---

## 📥 Download Standalone

For users who don't want to install Python, you can download the latest pre-compiled version for Windows:

*   **[Download .exe (Portable)](https://github.com/yashpalsinghsarangdevot/Media-Downloader-by-Yash/releases/latest)** - Single file, just run it.
*   **[Download .zip (Full Package)](https://github.com/yashpalsinghsarangdevot/Media-Downloader-by-Yash/releases/latest)** - Recommended if the portable version has issues.

---

## 🛠️ How to Use

1.  **Analyze Link:** Paste any supported media URL (YouTube, Instagram, etc.) and click **ANALYZE LINK**.
2.  **Select Quality:** Once analyzed, pick your preferred resolution or bitrate from the dropdown menu.
3.  **Choose Category:** Select **Video** (full clip), **Audio Only** (music), or **Video-Only**.
4.  **Trimming (Optional):** Check "Enable Trimming" and enter your desired segment times.
5.  **Extract:** Click **DOWNLOAD NOW** to start the process.
6.  **Track:** Monitor progress in real-time on the main page, and view your completed files in the **Finished Clips** tab.

---

## 📸 UI Preview

<p align="center">
  <img src="./assets/gui_preview.png" width="800" alt="Media Downloader UI Preview">
</p>

---

## 📖 Detailed Description

**Media Downloader by Yash** is an advanced multimedia tool designed to bridge the gap between complex command-line extraction utilities and the need for a streamlined, user-friendly desktop experience. Built on the industry-leading foundations of `yt-dlp` and `FFmpeg`, this application provides a robust environment for capturing, processing, and organizing digital content from over 1,000+ supported platforms.

In an era where digital content is fragmented across numerous services, this tool serves as a centralized hub for content creators, researchers, and media enthusiasts. It doesn't just "download" files; it intelligently analyzes media streams to provide the highest possible quality while offering granular control over the final output. Whether you are archiving high-resolution 4K video, extracting high-fidelity 320kbps audio for production, or precisely trimming a specific segment from a massive livestream, the engine handles the technical heavy lifting in the background.

### Technical Excellence & Architecture
The core of the application is built using a multi-threaded architecture in Python and PyQt6, ensuring that the user interface remains responsive even during heavy network operations. 

- **Intelligent Stream Selection:** Unlike basic downloaders, this tool utilizes a complex scoring system to automatically select the best video and audio streams, ensuring maximum compatibility with MP4/M4A containers.
- **Precision Engineering:** The segment trimming feature utilizes FFmpeg's keyframe-aware cutting, allowing users to extract exact moments from long-form content without the need for external editing software.
- **Bot Bypass & Resilience:** To combat aggressive bot detection on platforms like YouTube, the tool implements advanced network strategies, including IPv4 forcing (to bypass IPv6 subnet bans), user-agent rotation, and support for authenticated cookie sessions.

---


## 🚀 Key Features

### 🎞️ Ultra-HD Video Extraction
*   **No Resolution Limits:** Download in 4K (2160p), 1440p, 1080p, and more.
*   **Smart Containers:** Automatically selects the best format (MKV or MP4) to preserve original quality.
*   **Video-Only Mode:** Extract high-res visuals without audio for professional video editing.

### 🎵 High-Fidelity Audio
*   **Pure Sound:** Extract audio-only tracks at the highest available bitrate (up to 320kbps).
*   **Dynamic Selection:** Choose from multiple available bitrates and formats based on the source.

### ✂️ Precision Trimming
*   **Segment Extraction:** Built-in FFmpeg support allows you to download only specific parts of a video by setting exact Start and End times (HH:MM:SS).

### 🗂️ Persistent History & Retry
*   **Never Lose a Link:** All downloads are automatically saved to a local history file.
*   **One-Click Retry:** Instantly reload failed downloads or repeat past tasks with a single click.
*   **Detailed View:** Large, scrollable rows with hover-tooltips for easy tracking of filenames and paths.

### 🎨 Modern UI/UX
*   **Streamlined Tabs:** Clean 3-tab layout (Link Analyzer, Finished Clips, User Manual).
*   **High-Speed Core:** Native sharding technology maxes out your local bandwidth for faster downloads.

---

### 🌐 Supported Platforms
*   **Video:** YouTube (4K/8K), Instagram (Reels), TikTok, Vimeo, Facebook, Twitter (X), Reddit, LinkedIn, Dailymotion, etc.
*   **Audio:** SoundCloud, Mixcloud, Bandcamp, and more.
*   **Gaming:** Twitch (Clips/VODs), Kick.

---

## 🛠️ Installation (Development)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yashpalsinghsarangdevot/Media-Downloader-by-Yash.git
   cd Media-Downloader-by-Yash
   ```

2. **Install dependencies:**
   ```bash
   pip install pyqt6 yt-dlp pillow
   ```

3. **Ensure Binaries are present:**
   Place `ffmpeg.exe`, `ffprobe.exe`, `yt-dlp.exe`, and `deno.exe` in the project root.

4. **Run the app:**
   ```bash
   python launch.py
   ```

## 📦 Building Standalone Executable

To generate the single-file distribution, use the following PyInstaller command:

```bash
pyinstaller --noconfirm --onefile --windowed --name "Media Downloader by Yash" --icon "assets/logo.png" --add-binary "ffmpeg.exe;." --add-binary "ffprobe.exe;." --add-binary "deno.exe;." --add-binary "yt-dlp.exe;." --add-data "assets;assets" launch.py
```

## 👤 Author & Support

<p align="left">
  <a href="https://github.com/yashpalsinghsarangdevot" target="_blank">
    <img src="./assets/github.png" width="30" alt="GitHub"> <b>GitHub</b>
  </a>
  &nbsp;&nbsp;&nbsp;
  <a href="https://instagram.com/yashhpalsingh_sarangdevot" target="_blank">
    <img src="./assets/instagram.webp" width="30" alt="Instagram"> <b>Instagram</b>
  </a>
</p>

**Developed with ❤️ by Yashpal Singh Sarangdevot**

---

## ⚖️ License & Ethics

This software is provided for educational and personal archival purposes. Users are responsible for complying with the Terms of Service of the platforms they interact with. Please support content creators by consuming their work through official channels.
