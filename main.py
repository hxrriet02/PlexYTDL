# Imports
from __future__ import unicode_literals # For YouTube-DL
import urllib.request, json, os, youtube_dl, ffmpeg, subprocess

# My modules
import setup, scanner

# Variable
AudioTypes = ["webm", "m4a"]
VideoTypes = ["mp4", "webm"]

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
    setup.settings()


# Allows settings to easily be accessed
with open("settings.json", "r") as f:
    settings = json.loads(f.read())

# Starts scanning for videos
scanner.start()

# Download all videos
with open("videos.json") as f:
    AllVideos = json.loads(f.read())

# Loops through each video in videos.json
for video in AllVideos:
    # Get needed information
    VideoID = video["video_id"]
    VideoChannel = video["channel_name"]
    VideoReleaseDate = video["video_release_date"]

    TempDir = settings["temp_dir"]
    TempPath = f"{TempDir}/{VideoChannel}/{VideoReleaseDate} [{VideoReleaseDate}]"
    OutputDir = settings["output_dir"]
    OutputPath = f"{OutputDir}/{VideoChannel}/{VideoReleaseDate} [{VideoReleaseDate}]"

    # Download thumbnail
    if not os.path.exists(OutputPath + ".jpg"): # Checks if the thumbnail needs to be downloaded
        try:
            os.makedirs(f"{OutputDir}/{VideoChannel}/")
        except Exception:
            pass

        urllib.request.urlretrieve(video["video_thumbnail_url"], OutputPath + ".jpg")

    ##############################
    #                            #
    #       Download video       #
    #                            #
    ##############################

    if not os.path.exists(OutputPath + ".mp4"):
        # Video only
        VideoOptions = {
            "format": "bestvideo",
            "outtmpl": f"{TempPath} (video).%(ext)s"
        }

        with youtube_dl.YoutubeDL(VideoOptions) as ytdlv:
            ytdlv.download([f"https://www.youtube.com/watch?v={VideoID}"])

        # Audio only
        AudioOptions = {
            "format": "bestaudio/best",
            "outtmpl": f"{TempPath} (audio).%(ext)s"
        }

        with youtube_dl.YoutubeDL(AudioOptions) as ytdla:
            ytdla.download([f"https://www.youtube.com/watch?v={VideoID}"])

        # Converting audio to mp3 format
        for ext in AudioTypes:
            if os.path.exists(f"{TempPath} (audio).mp3"):
                pass
            elif os.path.exists(f"{TempPath} (audio).{ext}"):
                input = f"{TempPath} (audio).{ext}"
                cmd(f'ffmpeg -i "{input}" -vn -f mp3 "{TempPath} (audio).mp3"')

        AudioOnlyPath = f"{TempPath} (audio).mp3"

        # Finding downloaded video file
        for ext in VideoTypes:
            if os.path.exists(f"{TempPath} (video).{ext}"):
                VideoOnlyPath = f"{TempPath} (video).{ext}"

        # Combines audio and video into one file
        # Old .mkv output that needs a plex agent to get metadata
        cmd(f'ffmpeg -i "{VideoOnlyPath}" -i "{AudioOnlyPath}" -c copy "{OutputPath}.mkv"')

        # New one that uses local metadata to function
        #cmd(f'ffmpeg -i "{VideoOnlyPath}" -i "{AudioOnlyPath}" -c copy "{OutputPath}.mp4"' +
        #        f' -metadata title="{video["video_title"]}"' +
        #        f' -metadata description="{video["video_description"]}"' +
        #        f' -metadata year+{video["video_release_date"].split("-")[0]}'
        #        )
        # .outputOptions("-metadata", "title="+video.shortTitle, "-metadata", "AUTHOR="+video.subChannel, "-metadata", "YEAR="+Date(video.releaseDate), "-metadata", "description="+video.description, "-metadata", "synopsis="+video.description, "-strict", "-2")


        # Delete audio and video only files.
        files = os.listdir(f"{TempDir}")

        for file in files:
            if ("(audio)" in file) or ("(video)" in file):
                if VideoID in file:
                    os.remove(f"{channel}/{file}")
