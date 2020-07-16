# Imports
from __future__ import unicode_literals # For YouTube-DL
import urllib.request, json, os, youtube_dl, ffmpeg, subprocess

# My modules
import downloader, setup, scanner


def cmd(command):
    subprocess.call(command)

# Check if the correct files exist
if not os.path.exists("videos.json"):
    with open("videos.json", "w") as file:
        file.write("[]")

if not os.path.exists("channels.json"):
    with open("channels.json", "w") as file:
        file.write("[]")

if not os.path.exists("settings.json"):
    setup.installPip()
    setup.settings()


# Allows settings to easily be accessed
with open("settings.json", "r") as f:
    settings = json.loads(f.read())

# Starts scanning for videos
scanner.start()

# Download all videos
downloader.videos(settings)
