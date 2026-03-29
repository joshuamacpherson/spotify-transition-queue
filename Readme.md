# Spotify Shuffle Transition Queue

When listening on shuffle, certain songs are meant to transition into each other
— but shuffle ruins that. This tool lets you group songs into "folders", and
whenever shuffle plays the first song, the rest of the folder is automatically
queued in order.

## Prerequisites

- Python 3.10+
- A [Spotify Developer](https://developer.spotify.com/dashboard) account
- Your playlist must be on shuffle

## Setup

1. Clone the repository

   git clone https://github.com/joshuamacpherson/spotify-transition-queue

2. Create a Spotify Developer app at https://developer.spotify.com/dashboard
   - Set the redirect URI to `http://localhost:8888/callback`
   - Copy your Client ID and Client Secret

3. Create a `.env` file in the root directory based on `.env.example`:

   SPOTIPY_CLIENT_ID=your_client_id
   SPOTIPY_CLIENT_SECRET=your_client_secret
   SPOTIPY_REDIRECT_URI=http://localhost:8888/callback

4. Run `setup.bat` to create the virtual environment and build the executable:

   setup.bat

5. Run `play.bat` to start the app, or run `main.exe` directly.

## Usage

The app runs in your system tray. Click **Start Listening** to begin monitoring
your playback, and **Stop Listening** to pause it.

Use `play.bat` followed by a command to manage your folders via the CLI.

### Folders

| Command                          | Description          |
|----------------------------------|----------------------|
| `play.bat folder create "name"`  | Create a folder      |
| `play.bat folder remove "name"`  | Remove a folder      |

### Tracks

| Command                                              | Description                        |
|------------------------------------------------------|------------------------------------|
| `play.bat track add "folder"`                        | Add currently playing track        |
| `play.bat track add "folder" "search query"`         | Add track by search                |
| `play.bat track add "folder" "spotify URL"`          | Add track by Spotify URL           |
| `play.bat track remove "folder" "track name"`        | Remove a track                     |
| `play.bat track remove "folder" all`                 | Remove all tracks from a folder    |

### Playlists

| Command                               | Description                          |
|---------------------------------------|--------------------------------------|
| `play.bat playlist add "link"`        | Register a playlist to monitor       |
| `play.bat playlist remove "link"`     | Unregister a playlist                |
| `play.bat playlist liked-songs true`  | Enable monitoring of liked songs     |
| `play.bat playlist liked-songs false` | Disable monitoring of liked songs    |

### Display

| Command                          | Description                    |
|----------------------------------|--------------------------------|
| `play.bat display all`           | Show all folders and tracks    |
| `play.bat display folders`       | Show all folders               |
| `play.bat display songs "folder"`| Show tracks in a folder        |

<img width="256" height="118" alt="image" src="https://github.com/user-attachments/assets/2c58cafb-b843-47ce-a8ef-a88fc73f8dc4" />

<img width="1101" height="423" alt="image" src="https://github.com/user-attachments/assets/f8480797-9a5c-41dc-a35a-b3bf0546ae75" />
<img width="476" height="423" alt="image" src="https://github.com/user-attachments/assets/4bde3d69-06bb-4b85-b621-204e56b48eef" />

## License

MIT
