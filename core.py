import json
from pathlib import Path

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

DATA_FILE = Path("folders.json")
load_dotenv()

scope = "user-library-read user-read-currently-playing playlist-read-private user-modify-playback-state user-read-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def load_data():
    if not DATA_FILE.exists():
        return {"playlists": [], "allow_liked_songs": False, "folders": []}
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    if "playlists" not in data:
        data["playlists"] = []
        save_data(data)
    if "allow_liked_songs" not in data:
        data["allow_liked_songs"] = False
        save_data(data)
    return data


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def find_folder(data, folder_name: str):
    for f in data["folders"]:
        if f["name"] == folder_name:
            return f
    return None


def find_track(data, name: str, artist: str):
    for folder in data["folders"]:
        for i, track in enumerate(folder["tracks"]):
            if track["name"] == name and track["artist"] == artist:
                return folder, i, len(folder["tracks"])
    return None, None, None


def new_track(id: str, name: str, artist: str):
    return {"id": id, "name": name, "artist": artist}


def parse_query(query: str):
    if "open.spotify.com/track/" in query:
        track_id = query.split("/track/")[1].split("?")[0]
        return "id", track_id
    else:
        raise ValueError("Invalid track URL.")


def parse_playlist(query: str):
    if "open.spotify.com/playlist/" in query:
        playlist_id = query.split("/playlist/")[1].split("?")[0]
        return f"spotify:playlist:{playlist_id}"
    elif query.startswith("spotify:playlist:"):
        return query
    else:
        raise ValueError("Invalid playlist URL.")
