import os
import re
import subprocess
import time

from lrclib import LrcLibAPI


ANSI_CLEAR = "\033[2J\033[H"
ANSI_BOLD = "\033[1m"
ANSI_CYAN = "\033[96m"
ANSI_DIM = "\033[2m"
ANSI_REVERSE = "\033[7m"
ANSI_RESET = "\033[0m"

lyrics_api = LrcLibAPI(user_agent="auto-lyrics/1.0 (https://github.com/yourname/auto-lyrics)")

def clear_screen():
    print(ANSI_CLEAR, end="", flush=True)


def get_spotify_status():
    try:
        artist = subprocess.check_output(
            ["playerctl", "-p", "spotify", "metadata", "artist"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()

        title = subprocess.check_output(
            ["playerctl", "-p", "spotify", "metadata", "title"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()

        return artist, title

    except subprocess.CalledProcessError:
        return None, None


def get_spotify_position():
    try:
        raw = subprocess.check_output(
            ["playerctl", "-p", "spotify", "position"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        return float(raw) if raw else 0.0
    except (subprocess.CalledProcessError, ValueError):
        return 0.0


def get_spotify_duration():
    try:
        raw = subprocess.check_output(
            ["playerctl", "-p", "spotify", "metadata", "mpris:length"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        if not raw:
            return 0
        return float(raw) / 1_000_000.0
    except (subprocess.CalledProcessError, ValueError):
        return 0


def parse_synced_lyrics(raw_lyrics):
    entries = []
    if not raw_lyrics:
        return entries

    for line in raw_lyrics.splitlines():
        match = re.match(r"\[(\d+):(\d+(?:\.\d+)?)\]\s*(.*)", line.strip())
        if not match:
            continue

        minutes, seconds, text = match.groups()
        time_value = int(minutes) * 60 + float(seconds)
        text = text.strip()
        if text:
            entries.append({"time": time_value, "text": text})

    return entries


def render_lyric_window(song_title, artist_name, synced_lines, current_position):
    clear_screen()
    print(f"{ANSI_BOLD}{song_title}{ANSI_RESET} by {ANSI_CYAN}{artist_name}{ANSI_RESET}\n")

    if not synced_lines:
        print("No synced lyrics available for this track.")
        return

    active_index = 0
    for index, entry in enumerate(synced_lines):
        if current_position < entry["time"]:
            active_index = max(0, index - 1)
            break
    else:
        active_index = len(synced_lines) - 1

    prev_line = synced_lines[active_index - 1]["text"] if active_index > 0 else ""
    current_line = synced_lines[active_index]["text"]
    next_line = synced_lines[active_index + 1]["text"] if active_index + 1 < len(synced_lines) else ""

    if prev_line:
        print(f"{ANSI_DIM}{prev_line}{ANSI_RESET}")
    else:
        print()

    print(f"{ANSI_REVERSE}{ANSI_BOLD}{current_line}{ANSI_RESET}")

    if next_line:
        print(f"{ANSI_DIM}{next_line}{ANSI_RESET}")
    else:
        print()


def animate_karaoke_lyrics(song_title, artist_name, synced_lines):
    if not synced_lines:
        clear_screen()
        print(f"{ANSI_BOLD}{song_title}{ANSI_RESET} by {ANSI_CYAN}{artist_name}{ANSI_RESET}\n")
        print("No synced lyrics available for this track.")
        return

    while True:
        current_position = get_spotify_position()
        current_artist, current_title = get_spotify_status()

        if not current_title or not current_artist:
            break

        if current_title != song_title or current_artist != artist_name:
            break

        render_lyric_window(song_title, artist_name, synced_lines, current_position)
        time.sleep(0.35)

    print("\n" + "-" * 40)


def get_lyrics(song_title, artist_name):
    try:
        duration = int(get_spotify_duration())
        lyrics = lyrics_api.get_lyrics(
            track_name=song_title,
            artist_name=artist_name,
            album_name="",
            duration=duration,
            cached=False,
        )

        if lyrics and lyrics.synced_lyrics:
            synced_lines = parse_synced_lyrics(lyrics.synced_lyrics)
            if synced_lines:
                animate_karaoke_lyrics(song_title, artist_name, synced_lines)
                return

        print(f"No synced lyrics found for '{song_title}' by {artist_name}.")
    except Exception as e:
        print(f"Could not fetch synced lyrics for '{song_title}' by {artist_name}: {e}")


def main():
    current_track = None

    print("Listening for Spotify track changes\n")

    while True:
        artist_name, song_title = get_spotify_status()

        if song_title and artist_name:
            track_identifier = f"{artist_name} - {song_title}"

            if track_identifier != current_track:
                current_track = track_identifier
                get_lyrics(song_title, artist_name)
        else:
            if current_track is not None:
                print("\n[Spotify paused or closed]")
                current_track = None
                break

        time.sleep(2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped lyric auto-fetcher.")