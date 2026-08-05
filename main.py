import os
import subprocess
import time
import lyricsgenius
from requests.exceptions import Timeout


TOKEN = ""


def get_spotify_status():
    try:

        artist = subprocess.check_output(
            ["playerctl", "-p", "spotify", "metadata", "artist"], 
            stderr=subprocess.DEVNULL
        ).decode().strip()

        title = subprocess.check_output(
            ["playerctl", "-p", "spotify", "metadata", "title"], 
            stderr=subprocess.DEVNULL
        ).decode().strip()

        return artist, title

    except subprocess.CalledProcessError:
        print("Spotify desktop app is not open or nothing is currently loaded.")
        return None,None




genius = lyricsgenius.Genius(
    TOKEN, 
    timeout=15,   
    retries=3      
)

genius.verbose = True
genius.remove_section_headers = False

def get_lyrics(song_title, artist_name):
    try:
        song = genius.search_song(song_title, artist_name)
        if song:
            os.system("clear")
            print(f"--- {song.title} by {song.artist} ---\n")
            print(song.lyrics)
        else:
            print(f"Could not find lyrics for '{song_title}' by {artist_name}.")
    except Timeout:
        print("Error: The request to Genius timed out. Check your internet connection or try again.")
    except Exception as e:
        print(f"An error occurred: {e}")



def main():
    current_track = None

    print("Listening for Spotify track changes\n")

    while True:
        artist_name, song_title = get_spotify_status()

        if song_title and artist_name:
            # Combine into a unique identifier for the track
            track_identifier = f"{artist_name} - {song_title}"

            # Only fetch lyrics if the track has changed
            if track_identifier != current_track:
                current_track = track_identifier
                get_lyrics(song_title, artist_name)
        else:
            # Clear stored track if Spotify is paused or closed
            if current_track is not None:
                print("\n[Spotify paused or closed]")
                current_track = None
                break

        # Check for track changes every 3 seconds
        time.sleep(3)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped lyric auto-fetcher.")