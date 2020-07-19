import json, urllib, os, subprocess, re, youtube_dl, logger

# Variable
AudioTypes = ["webm", "m4a"]
VideoTypes = ["mp4", "webm"]

def FixText(string):
    return string.replace('\\\\', '\\\\\\\\').replace('"', '\\"').replace("'", "\\'").replace("\u2013", "-")

def artwork(ChannelID, ChannelName, settings, UseID = True):
    api_key = settings["api_key"]
    if UseID == True:
        query = f"https://www.googleapis.com/youtube/v3/channels/?part=snippet,statistics,brandingSettings&key={api_key}&id={ChannelID}"
    else:
        query = f"https://www.googleapis.com/youtube/v3/channels/?part=snippet,statistics,brandingSettings&key={api_key}&forUsername={ChannelID}"

    with urllib.request.urlopen(query) as request:
        rawJson = json.load(request)["items"][0]

    # Download Logo
    if not os.path.exists(f'{settings["output_dir"]}/{ChannelName}/poster.jpg'):
        logger.log("poster.jpg does not exist, downloading it")
        logo = rawJson["snippet"]["thumbnails"]["high"]["url"]
        image(logo, f'{settings["output_dir"]}/{ChannelName}', 'poster.jpg')

    # Download background
    if not os.path.exists(f'{settings["output_dir"]}/{ChannelName}/background.jpg'):
        logger.log("background.jpg does not exist, downloading it")
        background = rawJson["brandingSettings"]["image"]["bannerTvImageUrl"]
        image(background, f'{settings["output_dir"]}/{ChannelName}', 'background.jpg')

    # Download banner
    if not os.path.exists(f'{settings["output_dir"]}/{ChannelName}/banner.jpg'):
        logger.log("banner.jpg does not exist, downloading it")
        banner = rawJson["brandingSettings"]["image"]["bannerTabletExtraHdImageUrl"]
        image(banner, f'{settings["output_dir"]}/{ChannelName}', 'banner.jpg')

def image(url, dir, fileName):
    try:
        os.makedirs(dir)
    except Exception:
        pass

    urllib.request.urlretrieve(url, f"{dir}/{fileName}")

def videos(settings):
    with open("videos.json") as f:
        AllVideos = json.loads(f.read())

    logger.log(f"\n\nDownloading videos from 'videos.json'")

    # Loops through each video in videos.json
    for video in AllVideos:
        # Get needed information
        VideoID = video["video"]["id"]
        VideoChannel = video["channel_name"]
        VideoReleaseDate = video["video"]["release_date"]
        VideoFileTitle = re.sub(r"\W+", " ", video["video"]["title"])

        TempDir = settings["temp_dir"]
        TempPath = f"{TempDir}/{VideoChannel}/{VideoReleaseDate} {VideoFileTitle}"
        OutputDir = settings["output_dir"]
        OutputPath = f"{OutputDir}/{VideoChannel}/{VideoReleaseDate} {VideoFileTitle}"

        logger.log(f"Downloading: '" + video["channel_name"] + "' - '" + VideoFileTitle + "'", "\n")

        if not os.path.exists(f"{OutputPath}.mp4"):
            # Download logo, background and banner
            # Only downloads if "download_channel_art" is set to true in settings
            if settings["download_channel_art"] == True:
                artwork(video["channel_id"], VideoChannel, settings)
                logger.log("  - Download channel art is enabled, attempting to download art")
            else:
                logger.log("  - Download channel art is disabled, skipping")

            # Download thumbnail
            if not os.path.exists(OutputPath + ".jpg") and settings["download_thumbnails"] == True: # Checks if the thumbnail needs to be downloaded
                logger.log("  - Downloading thumbnails")
                try:
                    os.makedirs(f"{OutputDir}/{VideoChannel}/")
                except Exception:
                    pass

                urllib.request.urlretrieve(video["video"]["thumbnail_url"], OutputPath + ".jpg")
            else:
                logger.log("  - Skipping thumbnail download, path already exists or setting disabled")

            # Download subtitles
            if settings["download_subtitles"] == True:
                logger.log("  - Downloading subtitles")
                SubtitleOptions = {
                    "writesubtitles": True,
                    "skip_download": True,
                    "allsubtitles": True,
                    "outtmpl": f"{OutputPath}.%(ext)s"
                }

                with youtube_dl.YoutubeDL(SubtitleOptions) as subs:
                    subs.download([f"https://www.youtube.com/watch?v={VideoID}"])
            else:
                logger.log("  - Skipping subtitles download, setting disabled")

            ##############################
            #                            #
            #       Download video       #
            #                            #
            ##############################


            logger.log("  - Downloading best video")

            # Video only
            VideoOptions = {
                "format": "bestvideo",
                "outtmpl": f"{TempPath} (video).%(ext)s"
            }

            with youtube_dl.YoutubeDL(VideoOptions) as ytdlv:
                ytdlv.download([f"https://www.youtube.com/watch?v={VideoID}"])

            # Audio only
            logger.log("  - Downloading best audio")
            AudioOptions = {
                "format": "bestaudio/best",
                "outtmpl": f"{TempPath} (audio).%(ext)s"
            }

            with youtube_dl.YoutubeDL(AudioOptions) as ytdla:
                ytdla.download([f"https://www.youtube.com/watch?v={VideoID}"])

            # Converting audio to mp3 format
            logger.log("  - Converting audio to mp3 format")
            for ext in AudioTypes:
                if os.path.exists(f"{TempPath} (audio).mp3"):
                    pass
                elif os.path.exists(f"{TempPath} (audio).{ext}"):
                    input = f"{TempPath} (audio).{ext}"
                    subprocess.call(f'ffmpeg -i "{input}" -vn -f mp3 "{TempPath} (audio).mp3"')

            AudioOnlyPath = f"{TempPath} (audio).mp3"

            # Finding downloaded video file
            for ext in VideoTypes:
                if os.path.exists(f"{TempPath} (video).{ext}"):
                    VideoOnlyPath = f"{TempPath} (video).{ext}"

            # Combines audio and video into one file
            logger.log("  - Combining audio and video into one file using ffmpeg")
            subprocess.call(f'ffmpeg -i "{VideoOnlyPath}" -i "{AudioOnlyPath}"' +
                    f' -metadata title="{FixText(video["video"]["title"])}"' +
                    f' -metadata author="{FixText(video["channel_name"])}"' +
                    f' -metadata description="{FixText(video["video"]["description"])}"' +
                    f' -metadata year={video["video"]["release_date"]}' +
                    f' -c copy "{OutputPath}.mp4"')

            # Delete audio and video only files.
            # {os.getcwd()}/
            files = os.listdir(f"{TempDir}")

            if os.path.exists(OutputPath + ".mp4"):
                logger.log("  - Deleting audio only and video only files")
                for file in files:
                    if ("(audio)" in file) or ("(video)" in file):
                        if VideoFileTitle in file:
                            # os.remove(f"{TempDir}/{file}")
                            print(f"{TempDir}/{file}")
        else:
            logger.log("  - Video already downloaded, skipping")
