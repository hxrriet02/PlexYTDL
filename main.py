# Imports
from __future__ import unicode_literals # For YouTube-DL
import urllib.request, json, os, youtube_dl, ffmpeg, time, re, subprocess
from time import gmtime, strftime
from shutil import copyfile

# My modules
import setup, scanner

# Check if the correct files exist
if not os.path.exists("videos.json"):
    with open("videos.json", "w") as file:
        file.write("[]")

if not os.path.exists("channels.json"):
    with open("channels.json", "w") as file:
        file.write("[]")

if not os.path.exists("settings.json"):
    setup.settings()

# Starts scanning for videos
scanner.start()
