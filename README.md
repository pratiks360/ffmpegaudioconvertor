<p align="center">
  <h1 align="center">🎵 FFmpeg Audio Converter</h1>
  <p align="center">
    <strong>A lightweight REST API that converts and re-encodes WAV audio files using FFmpeg — deployable anywhere with Docker.</strong>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python 3">
    <img src="https://img.shields.io/badge/Flask-REST_API-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
    <img src="https://img.shields.io/badge/FFmpeg-Powered-007808?style=for-the-badge&logo=ffmpeg&logoColor=white" alt="FFmpeg">
    <img src="https://img.shields.io/badge/Docker-Ready-2496ed?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
    <img src="https://img.shields.io/github/last-commit/pratiks360/ffmpegaudioconvertor?style=for-the-badge&label=Last+Commit" alt="Last Commit">
  </p>
</p>

---

## 📋 Table of Contents

- [What Is This?](#-what-is-this)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [API Reference](#-api-reference)
- [How It Works](#-how-it-works)
- [Tech Stack](#️-tech-stack)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ What Is This?

**FFmpeg Audio Converter** is a minimal Flask REST API that accepts a WAV file upload and re-encodes it to 8-bit PCM WAV format using FFmpeg. It's containerized with Docker so you can spin it up in seconds — no local FFmpeg installation required.

> 💡 Useful for audio pipelines, preprocessing for voice/ML workloads, or anywhere you need server-side audio format normalization.

---

## 🎯 Features

| Feature | Description |
|---|---|
| 🎵 **WAV Re-encoding** | Converts uploaded WAV files to 8-bit unsigned PCM (`pcm_u8`) for compatibility with downstream systems |
| 🚀 **Simple REST API** | Single `/convert` endpoint — POST a file, get a file back |
| 🐳 **Docker-first** | One command to build and run; FFmpeg installed automatically in the container |
| 🧹 **Auto-cleanup** | Previous conversion result is removed before each new job to avoid stale file serving |
| ⚡ **Lightweight** | Minimal dependencies — just Flask and ffmpeg-python |

---

## 🚀 Quick Start

### Option A · Docker (Recommended)

```bash
# Clone the repo
git clone https://github.com/pratiks360/ffmpegaudioconvertor.git
cd ffmpegaudioconvertor

# Build the image
docker build -t ffmpeg-audio-convertor .

# Run the container
docker run -p 8443:8443 ffmpeg-audio-convertor
```

The API will be live at `http://localhost:8443`.

### Option B · Run Locally

**Prerequisites:** Python 3, FFmpeg installed on your system (`ffmpeg` in PATH)

```bash
git clone https://github.com/pratiks360/ffmpegaudioconvertor.git
cd ffmpegaudioconvertor

pip install -r requirements.txt
python app.py
```

---

## 📡 API Reference

### `GET /`

Health check — confirms the server is running.

**Response:** `200 OK` — `"booted UP!"`

---

### `POST /convert`

Upload a WAV file and receive a re-encoded 8-bit PCM WAV in response.

**Request:** `multipart/form-data` with a `file` field containing a `.wav` file.

```bash
curl -X POST http://localhost:8443/convert \
  -F "file=@your-audio.wav" \
  --output result.wav
```

| Case | Response |
|---|---|
| Success | `200 OK` — re-encoded `result.wav` file |
| No file field | `400` — `No file uploaded` |
| Empty filename | `400` — `No file selected` |
| Non-WAV file | No response (filtered by `allowed_file`) |

---

## 🧩 How It Works

```
┌─────────────┐   POST /convert    ┌─────────────┐   ffmpeg.input()   ┌─────────────┐
│             │  ────────────────► │             │  ────────────────► │             │
│   Client    │   WAV file upload  │  Flask API  │   pcm_u8 encode    │   FFmpeg    │
│             │  ◄────────────────  │             │  ◄────────────────  │             │
└─────────────┘   result.wav       └─────────────┘   result.wav        └─────────────┘
```

1. **Upload** — Client POSTs a `.wav` file to `/convert`
2. **Validate** — Flask checks the file exists and has a `.wav` extension
3. **Save** — File is written to disk as `temp.wav`
4. **Convert** — FFmpeg re-encodes to `result.wav` using `pcm_u8` codec with `--bitexact` for deterministic output
5. **Return** — `result.wav` is streamed back to the client with `audio/wav` MIME type

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3 |
| **Web Framework** | Flask |
| **Audio Processing** | FFmpeg via `ffmpeg-python` |
| **Containerization** | Docker |
| **Base Image** | `python:3` |

---

## 🔒 Notes

- Files are saved to the container's local filesystem (`temp.wav`, `result.wav`) — not persisted between container restarts
- The server runs on port `8443` with `debug=True` — change to `debug=False` for production
- Only `.wav` input is accepted; other formats will be silently rejected

---

## 🐛 Troubleshooting

**Q: `ffmpeg: command not found` when running locally**
A: Install FFmpeg on your system: `brew install ffmpeg` (macOS) or `apt-get install ffmpeg` (Ubuntu). Or just use Docker — it handles this automatically.

**Q: Getting `No file uploaded` error**
A: Make sure your request uses `multipart/form-data` and the field name is exactly `file`.

**Q: Container builds but crashes on start**
A: Check that port `8443` isn't already in use. Run `docker run -p 9000:8443 ffmpeg-audio-convertor` to use a different host port.

**Q: Output audio sounds wrong**
A: The converter re-encodes to 8-bit unsigned PCM (`pcm_u8`), which reduces bit depth. If you need higher fidelity, modify the `acodec` parameter in `app.py`.

---

## 🤝 Contributing

PRs and issues welcome! If you want to add support for more formats (MP3, FLAC, etc.) or improve error handling, feel free to open a PR.

---

## 📄 License

This project is open source and available for personal use.

---

<p align="center">
  <sub>Built with ❤️ for developers who need fast, containerized audio processing.</sub>
</p>
