# Auto Lyrics Karaoke

This project watches Spotify, fetches synced lyrics from LRCLIB, and displays them in a karaoke-style terminal view with:

- one previous line
- one highlighted current line
- one next line

It is designed for the Linux desktop Spotify flow using `playerctl`.

## Requirements

- Python 3.10+
- Spotify desktop app running
- `playerctl` installed
- Internet access

### Install `playerctl`

- Ubuntu/Debian: `sudo apt install playerctl`
- Fedora: `sudo dnf install playerctl`
- Arch: `sudo pacman -S playerctl`

## Setup

1. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the required packages:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install lrclibapi
   ```

3. Run the app:

   ```bash
   python main.py
   ```

4. Press `Ctrl+C` to stop it.

## Notes

- The script polls Spotify every few seconds.
- It matches the current playing track and fetches synced lyrics from LRCLIB.
- The active lyric line is highlighted while the neighboring lines remain visible.
- If Spotify is paused, closed, or no track is active, the app stops showing lyrics.

## Current behavior

This project does not use a Genius API token anymore. It uses the LRCLIB synced-lyrics service instead because it supports timestamped lyric lines that work much better for karaoke-style syncing.
