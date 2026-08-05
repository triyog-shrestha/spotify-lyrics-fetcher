# Genius Lyrics Auto-Fetcher

This script watches Spotify and automatically fetches lyrics from Genius for the currently playing track.

## Requirements

- Python 3.10 or newer
- A Genius API token
- Spotify Desktop running
- Internet access

### Linux

Install the Spotify metadata helper:

- Ubuntu/Debian: `sudo apt install playerctl`
- Fedora: `sudo dnf install playerctl`
- Arch: `sudo pacman -S playerctl`

### macOS and Windows

The current script uses `playerctl`, which is Linux-focused. It can still be run on other systems after adapting the Spotify detection part, but Linux is the recommended platform for full functionality.

## Setup

1. Create and activate a virtual environment.

   Linux/macOS:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   Windows PowerShell:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the required Python packages:
   ```bash
   pip install requests lyricsgenius
   ```

3. Put your own genius api 
   ```

4. Run the script:
   ```bash
   python genius.py
   ```

5. Press `Ctrl+C` to stop the script.

## Notes

- The script checks Spotify every few seconds.
- Lyrics are fetched when the track changes.
- If Spotify is paused, closed, or no track is active, the script will print a message instead of lyrics.
