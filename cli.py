from typing import Optional

import typer
from core import (
    find_folder,
    find_track,
    load_data,
    new_track,
    parse_playlist,
    parse_query,
    save_data,
    sp,
)

app = typer.Typer()
playlist_app = typer.Typer()
folder_app = typer.Typer()
track_app = typer.Typer()
display_app = typer.Typer()

app.add_typer(playlist_app, name="playlist")
app.add_typer(folder_app, name="folder")
app.add_typer(track_app, name="track")
app.add_typer(display_app, name="display")


# --- Display ---


@display_app.command("folders")
def display_folders():
    data = load_data()
    if not data["folders"]:
        typer.echo("No folders found.")
        return
    typer.echo("")
    for folder in data["folders"]:
        typer.echo(f"- {folder['name']}")
    typer.echo("")


@display_app.command("all")
def display_all():
    data = load_data()
    if not data["folders"]:
        typer.echo("No folders found.")
        return
    typer.echo("")
    for folder in data["folders"]:
        typer.echo(f"{folder['name']}:")
        if not folder["tracks"]:
            typer.echo("  (empty)")
        for track in folder["tracks"]:
            typer.echo(f"  {track['name']} - {track['artist']}")
        typer.echo("")


@display_app.command("songs")
def display_songs(folder_name: str):
    data = load_data()
    if (folder := find_folder(data, folder_name)) is None:
        typer.echo(f"Folder '{folder_name}' not found.")
        raise typer.Exit()
    if not folder["tracks"]:
        typer.echo(f"'{folder_name}' is empty.")
        return
    for track in folder["tracks"]:
        typer.echo(f"{track['name']} - {track['artist']}")


# --- Playlist ---


@playlist_app.command("add")
def playlist_add(playlist: str):
    data = load_data()
    try:
        uri = parse_playlist(playlist)
    except ValueError as e:
        typer.echo(str(e))
        raise typer.Exit()
    if uri in data["playlists"]:
        typer.echo("Playlist already added.")
        raise typer.Exit()
    data["playlists"].append(uri)
    save_data(data)
    typer.echo("Playlist added successfully.")


@playlist_app.command("remove")
def playlist_remove(playlist: str):
    data = load_data()
    try:
        uri = parse_playlist(playlist)
    except ValueError as e:
        typer.echo(str(e))
        raise typer.Exit()
    if uri not in data["playlists"]:
        typer.echo("Playlist not found.")
        raise typer.Exit()
    data["playlists"].remove(uri)
    save_data(data)
    typer.echo("Playlist removed.")


@playlist_app.command("liked-songs")
def playlist_liked_songs(enable: bool):
    data = load_data()
    data["allow_liked_songs"] = enable
    save_data(data)
    typer.echo(f"Liked songs {'enabled' if enable else 'disabled'}.")


# --- Folder ---


@folder_app.command("create")
def folder_create(folder_name: str):
    data = load_data()
    if any(f["name"] == folder_name for f in data["folders"]):
        typer.echo(f"Folder '{folder_name}' already exists.")
        raise typer.Exit()
    data["folders"].append({"name": folder_name, "tracks": []})
    save_data(data)
    typer.echo(f"Created folder '{folder_name}'.")


@folder_app.command("remove")
def folder_remove(folder_name: str):
    data = load_data()
    if find_folder(data, folder_name) is None:
        typer.echo(f"Folder '{folder_name}' not found.")
        raise typer.Exit()
    data["folders"] = [f for f in data["folders"] if f["name"] != folder_name]
    save_data(data)
    typer.echo(f"Removed folder '{folder_name}'.")


# --- Track ---


@track_app.command("add")
def track_add(
    folder_name: str,
    query: Optional[str] = typer.Argument(default=None),
):
    data = load_data()
    folder = find_folder(data, folder_name)
    if folder is None:
        typer.echo(f"Folder '{folder_name}' not found.")
        raise typer.Exit()

    if query is None:
        current = sp.current_user_playing_track()
        if current is None or not current["is_playing"]:
            typer.echo("Nothing is currently playing.")
            raise typer.Exit()
        track = current["item"]
    elif "open.spotify.com/track/" in query:
        try:
            _, track_id = parse_query(query)
        except ValueError as e:
            typer.echo(str(e))
            raise typer.Exit()
        track = sp.track(track_id)
    else:
        results = sp.search(q=query, type="track", limit=1)
        items = results["tracks"]["items"]
        if not items:
            typer.echo(f"No results found for '{query}'.")
            raise typer.Exit()
        track = items[0]

    folder["tracks"].append(
        new_track(track["id"], track["name"], track["artists"][0]["name"])
    )
    save_data(data)
    typer.echo(f"Added '{track['name']}' to '{folder_name}'.")


@track_app.command("remove")
def track_remove(
    folder_name: str,
    track_name: Optional[str] = typer.Argument(default=None),
):
    data = load_data()
    if (folder := find_folder(data, folder_name)) is None:
        typer.echo(f"Folder '{folder_name}' not found.")
        raise typer.Exit()
    if track_name is None:
        typer.echo("Please provide a song name or 'all'.")
        raise typer.Exit()
    if track_name == "all":
        if not typer.confirm(f"Remove all songs from '{folder_name}'?"):
            raise typer.Exit()
        folder["tracks"] = []
        save_data(data)
        typer.echo(f"Removed all songs from '{folder_name}'.")
        return

    original_length = len(folder["tracks"])
    folder["tracks"] = [t for t in folder["tracks"] if t["name"] != track_name]
    if len(folder["tracks"]) == original_length:
        typer.echo(f"'{track_name}' not found in '{folder_name}'.")
        raise typer.Exit()
    save_data(data)
    typer.echo(f"Removed '{track_name}' from '{folder_name}'.")


if __name__ == "__main__":
    app()
