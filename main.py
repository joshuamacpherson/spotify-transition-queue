import threading
import time

import pystray
from PIL import Image, ImageDraw

from core import find_track, load_data, sp

listen_thread: threading.Thread | None = None
stop_event = threading.Event()


def create_icon_image(color="green"):
    img = Image.new("RGB", (64, 64), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    fill = (0, 200, 0) if color == "green" else (200, 0, 0)
    draw.ellipse((8, 8, 56, 56), fill=fill)
    return img


def listen_loop(stop_event: threading.Event, icon: pystray.Icon):
    data = load_data()
    last_queued = None
    icon.icon = create_icon_image("green")

    while not stop_event.is_set():
        playback = sp.current_playback()
        if (
            playback is None
            or not playback["is_playing"]
            or not playback["shuffle_state"]
        ):
            stop_event.wait(5)
            continue

        context = playback["context"]
        if context is None:
            stop_event.wait(5)
            continue

        is_liked_songs = context["type"] == "collection" and data["allow_liked_songs"]
        in_playlist = context["uri"] in data["playlists"]

        if not is_liked_songs and not in_playlist:
            stop_event.wait(5)
            continue

        item = playback["item"]
        folder, position, folder_length = find_track(
            data, item["name"], item["artists"][0]["name"]
        )
        if folder is None:
            last_queued = None
            stop_event.wait(5)
            continue

        if folder["name"] == last_queued:
            stop_event.wait(5)
            continue

        for i in range(position + 1, folder_length):
            track = folder["tracks"][i]
            sp.add_to_queue(f"spotify:track:{track['id']}")

        last_queued = folder["name"]
        stop_event.wait(5)

    icon.icon = create_icon_image("red")


def start_listening(icon: pystray.Icon, item):
    global listen_thread, stop_event
    if listen_thread and listen_thread.is_alive():
        return
    stop_event = threading.Event()
    listen_thread = threading.Thread(
        target=listen_loop, args=(stop_event, icon), daemon=True
    )
    listen_thread.start()


def stop_listening(icon: pystray.Icon, item):
    stop_event.set()


def quit_app(icon: pystray.Icon, item):
    stop_event.set()
    icon.stop()


def main():
    menu = pystray.Menu(
        pystray.MenuItem("Start Listening", start_listening),
        pystray.MenuItem("Stop Listening", stop_listening),
        pystray.MenuItem("Quit", quit_app),
    )
    icon = pystray.Icon(
        "spotify-folders",
        create_icon_image("red"),
        "Spotify Folder Listener",
        menu,
    )

    def setup(icon):
        icon.visible = True
        time.sleep(0.5)
        start_listening(icon, None)

    icon.run(setup=setup)


if __name__ == "__main__":
    main()
