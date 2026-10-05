# Spotify lyrics fetcher

This project watches Spotify, fetches synced lyrics from LRCLIB, and displays them in a karaoke-style terminal view with:

- one previous line
- one highlighted current line
- one next line

It is designed for the Linux desktop Spotify flow using `playerctl`.

> **Windows note:** The current Python code calls the `playerctl` command directly.
> `playerctl` uses Linux MPRIS, so it is not a native Windows dependency. For
> Windows, use the WSL2 setup below, or adapt `main.py` to use a Windows media
> control API.

## Requirements

- Python 3.10+
- Spotify desktop app running
- `playerctl` installed
- Internet access

### Install `playerctl`

- Ubuntu/Debian: `sudo apt install playerctl`
- Fedora: `sudo dnf install playerctl`
- Arch: `sudo pacman -S playerctl`

## Windows setup (WSL2)

The simplest way to run the project on Windows is through WSL2. This requires
Windows 10 version 2004 or later, or Windows 11.

1. Open **PowerShell as Administrator** and install Ubuntu with WSL2:

   ```powershell
   wsl --install -d Ubuntu
   ```

   Restart Windows if prompted, then open the Ubuntu app and create your Linux
   user account.

2. In the Ubuntu terminal, install the dependencies:

   ```bash
   sudo apt update
   sudo apt install python3 python3-venv playerctl
   ```

3. From Ubuntu, go to the project directory. For example, if the project is
   stored in `C:\Users\YourName\Desktop\spotify-lyrics-fetcher`:

   ```bash
   cd /mnt/c/Users/YourName/Desktop/spotify-lyrics-fetcher
   ```

4. Create the virtual environment, install the Python package, and run the app:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install lrclibapi
   python main.py
   ```

   For `playerctl` to detect Spotify, Spotify must be running in the same Linux
   environment and expose MPRIS. On Windows 11, this can be done with a Linux
   Spotify desktop app through WSLg. The Windows Spotify desktop app does not
   normally expose MPRIS to WSL.

## Native Windows alternative to `playerctl`

There is no drop-in native Windows replacement that works with the current
code, because `main.py` has `playerctl` commands hard-coded. Windows users who
cannot use WSL2 need a small code change to read playback data through one of
these APIs instead:

- **Windows System Media Transport Controls (SMTC):** the native Windows
  media-session API; suitable for reading the currently playing Spotify track
  and playback position.
- **Spotify Web API:** works with the native Spotify app, but requires creating
  a Spotify developer application, OAuth authorization, and a user access token.

Installing a Windows command-line tool alone will not make the current version
work unless it provides a compatible executable named `playerctl` and returns
the same metadata and position output expected by `main.py`.

## Linux setup

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
