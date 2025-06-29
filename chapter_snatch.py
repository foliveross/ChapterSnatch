import re
import yt_dlp
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser

# 🎧 Set your Spotify credentials here directly
SPOTIPY_CLIENT_ID = "your_spotify_client_id"
SPOTIPY_CLIENT_SECRET = "your_spotify_client_secret"
SPOTIPY_REDIRECT_URI = "http://localhost:8888"
SCOPE = "playlist-modify-public"

sp = None
chapter_titles = []
playlist_file = ""

def generate_filename():
    current_dir = os.getcwd()
    existing_files = [file for file in os.listdir(current_dir) if file.endswith('.txt')]
    counter = 1
    for file in existing_files:
        if re.match(r'^\d+_', file):
            number = int(re.search(r'^(\d+)_', file).group(1))
            counter = max(counter, number + 1)
    current_datetime = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    return f"{counter:02d}_playlist_for_spotify_{current_datetime}.txt"

def extract_chapters(url):
    global chapter_titles, playlist_file
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        chapters = info.get('chapters', [])
    if not chapters:
        return None
    chapter_titles = [chapter['title'] for chapter in chapters]
    playlist_file = generate_filename()
    with open(playlist_file, 'w', encoding='utf-8') as f:
        for title in chapter_titles:
            f.write(f"{title}\n")
    return playlist_file

def authenticate_spotify():
    global sp
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        open_browser=True,
        cache_path=".cache"
    )
    token_info = sp_oauth.get_access_token(as_dict=False)
    sp = spotipy.Spotify(auth=token_info)

def search_and_prompt_playlist():
    global sp, chapter_titles, playlist_file
    if not chapter_titles:
        return

    if not sp:
        authenticate_spotify()

    found_tracks = []
    with open(playlist_file, 'a', encoding='utf-8') as f:
        f.write("\n--- Spotify Matches ---\n")
        for title in chapter_titles:
            result = sp.search(q=title, type='track', limit=1)
            tracks = result['tracks']['items']
            if tracks:
                track = tracks[0]
                uri = track['uri']
                name = track['name']
                artist = track['artists'][0]['name']
                found_tracks.append(uri)
                f.write(f"{name} - {artist}\n")
            else:
                f.write(f"Not found: {title}\n")

    if found_tracks:
        create = messagebox.askyesno("Create Playlist", "Multiple tracks found. Create a public playlist on Spotify?")
        if create:
            user_id = sp.me()['id']
            playlist_name = f"Auto Playlist {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
            sp.playlist_add_items(playlist_id=playlist['id'], items=found_tracks)
            webbrowser.open(playlist['external_urls']['spotify'])
            messagebox.showinfo("Playlist Created", f"Playlist created and opened in your browser:\n{playlist['external_urls']['spotify']}")

def run_gui():
    def on_extract():
        url = url_entry.get().strip()
        if not url:
            messagebox.showwarning("Missing URL", "Please enter a YouTube video URL.")
            return
        try:
            output = extract_chapters(url)
            if output:
                messagebox.showinfo("Success", f"Chapters saved to:\n{output}")
                search = messagebox.askyesno("Search on Spotify", "Do you want to search these chapters as songs on Spotify?")
                if search:
                    search_and_prompt_playlist()
            else:
                messagebox.showinfo("No Chapters", "No chapters found in this video.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

    root = tk.Tk()
    root.title("ChapterSnatch")
    tk.Label(root, text="YouTube Video URL:").pack(pady=(10, 2))
    url_entry = tk.Entry(root, width=60)
    url_entry.pack(padx=10, pady=2)
    tk.Button(root, text="Extract Chapters", command=on_extract).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
