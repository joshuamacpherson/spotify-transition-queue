# Spotify Shuffle Queue Fix

When listening to songs on shuffle in spotify, sometimes certain songs transition into other songs, and that gets ruined with shuffle. With this, group the 2 songs that transition together, and whenever the first song queues, the second one is automatically added to the queue.

**requires your own api key secret and callback all from spotify developer app!

Runs in the tray, click Start or Stop Listening to disable/enable it

<img width="256" height="118" alt="image" src="https://github.com/user-attachments/assets/2c58cafb-b843-47ce-a8ef-a88fc73f8dc4" />

<img width="1101" height="423" alt="image" src="https://github.com/user-attachments/assets/f8480797-9a5c-41dc-a35a-b3bf0546ae75" />
<img width="476" height="423" alt="image" src="https://github.com/user-attachments/assets/4bde3d69-06bb-4b85-b621-204e56b48eef" />




play.bat playlist add "link"
play.bat playlist remove "link"
play.bat playlist liked-songs

play.bat display all
play.bat display songs "folder"
play.bat display folders

play.bat track add "folder" "link" OR "title and artist/artist and title"
play.bat track remove "folder" "track_name" 
play.bat track remove "all"

play.bat folder create "name"
play.bat folder remove "folder_name"
