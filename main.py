# Imports
from __future__ import unicode_literals # For YouTube-DL
import urllib.request, json, os, youtube_dl, ffmpeg, subprocess, time

# My modules
import downloader, setup, scanner, logger


def cmd(command):
    subprocess.call(command)

# Start logging
logger.init()

# Check if the correct files exist
if not os.path.exists("videos.json"):
    logger.log("video.json does not exist, creating it now!")
    with open("videos.json", "w") as file:
        file.write("[]")

# if not os.path.exists("channels.json"):
#    log("channels.json does not exist, creating it now!")
#    with open("channels.json", "w") as file:
#        file.write("[]")

if not os.path.exists("settings.json"):
    logger.log("Attempting to download pip dependencies")
    setup.installPip()
    logger.log("'settings.json' does not exist, initiating setup now!")
    setup.settings()


# Allows settings to easily be accessed
with open("settings.json", "r") as f:
    settings = json.loads(f.read())


# For if "download_between_hours" is true
try:
    if settings["download_hours"]["download_between_hours"] == False:
        # Starts scanning for videos
        logger.log("Scanning starting", "\n\n")
        scanner.start()

        # Download all videos
        logger.log("Starting to download videos")
        downloader.videos(settings)
    else:
        while True:
            if int(settings["download_hours"]["time_start"]) < int(time.strftime("%H%M")) < int(settings["download_hours"]["time_end"]):
                # Starts scanning for videos
                log("\n\nStarting scanning")
                scanner.start()

                # Download all videos
                log("Starting to download videos")
                downloader.videos(settings)

            time.sleep(120)

    logger.end()
except Exception as e:
    logger.end(True, e)
