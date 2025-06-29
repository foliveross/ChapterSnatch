# 🎧 ChapterSnatch

**ChapterSnatch** is a Python GUI tool that extracts chapter titles from YouTube videos and optionally finds their matching songs on Spotify. It even lets you create a public Spotify playlist — no manual copying, no terminal hassle.

---

## 🚀 Features

- 🎬 Extract chapters from any YouTube video
- 🔎 Automatically search for songs on Spotify
- 🧠 OAuth login flow opens in your browser (no need to paste URLs)
- 🎵 Option to create a public playlist with found tracks
- 💾 Saves all titles and found songs into a `.txt` file
- 🖱️ Simple and intuitive graphical interface

---

## 🛠️ Requirements

### Python Packages

Install dependencies:

```bash
pip install yt-dlp spotipy
```

### Spotify Developer Setup

1. Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Set Redirect URI as:
   ```
   http://localhost:8888/callback
   ```
4. Copy your:
   - `Client ID`
   - `Client Secret`
5. Replace these values directly in the `chapter_snatch.py` script:

```python
SPOTIPY_CLIENT_ID = "your_spotify_client_id"
SPOTIPY_CLIENT_SECRET = "your_spotify_client_secret"
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"
```

> ✅ No need to set environment variables — all credentials are managed in the script.

---

## ▶️ How to Use

1. Run the script:

```bash
python chapter_snatch.py
```

2. Paste the YouTube video URL
3. Click **Extract Chapters**
4. When prompted, choose to:
   - Search matching songs on Spotify
   - Authenticate via browser login (once)
   - Create a public playlist if tracks are found

---

## 📁 Output Example

Filename:

```
03_playlist_for_spotify_29-06-2025_21-12-55.txt
```

Contents:

```
Intro
Track One
Track Two

--- Spotify Matches ---
Track One - Artist A
Track Two - Artist B
Not found: Intro
```

---

## 📜 License

MIT License — free for personal and commercial use.

---

## 👤 Author

Built with ❤️ by @foliveross

If you like it, consider starring the repo!
