import json, urllib, os, subprocess, re, youtube_dl

# Variable
AudioTypes = ["webm", "m4a"]
VideoTypes = ["mp4", "webm"]

def artwork(ChannelID, ChannelName, settings, UseID = True):
    api_key = settings["api_key"]
    if UseID == True:
        query = f"https://www.googleapis.com/youtube/v3/channels/?part=snippet,statistics,brandingSettings&key={api_key}&id={ChannelID}"
    else:
        query = f"https://www.googleapis.com/youtube/v3/channels/?part=snippet,statistics,brandingSettings&key={api_key}&forUsername={ChannelID}"

    with urllib.request.urlopen(query) as request:
        rawJson = json.load(request)["items"][0]

    # Download Logo
    logo = rawJson["snippet"]["thumbnails"]["high"]["url"]
    image(logo, f'{settings["output_dir"]}/{ChannelName}', 'poster.jpg')
    # Download background
    background = rawJson["brandingSettings"]["image"]["bannerTvImageUrl"]
    image(background, f'{settings["output_dir"]}/{ChannelName}', 'background.jpg')
    # Download banner
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

    # Loops through each video in videos.json
    for video in AllVideos:
        # Get needed information
        VideoID = video["video_id"]
        VideoChannel = video["channel_name"]
        VideoReleaseDate = video["video_release_date"]
        VideoFileTitle = re.sub(r"\W+", " ", video["video_title"])

        TempDir = settings["temp_dir"]
        TempPath = f"{TempDir}/{VideoChannel}/{VideoReleaseDate} {VideoFileTitle}"
        OutputDir = settings["output_dir"]
        OutputPath = f"{OutputDir}/{VideoChannel}/{VideoReleaseDate} {VideoFileTitle}"

        # Download logo, background and banner
        artwork(video["channel_id"], VideoChannel, settings)

        # Download thumbnail
        if not os.path.exists(OutputPath + ".jpg") and settings["download_thumbnails"] == True: # Checks if the thumbnail needs to be downloaded
            try:
                os.makedirs(f"{OutputDir}/{VideoChannel}/")
            except Exception:
                pass

            urllib.request.urlretrieve(video["video_thumbnail_url"], OutputPath + ".jpg")

        # Download subtitles
        if settings["download_subtitles"] == True:
            SubtitleOptions = {
                "writesubtitles": True,
                "skip_download": True,
                "allsubtitles": True,
                "outtmpl": f"{OutputPath}.%(ext)s"
            }

            with youtube_dl.YoutubeDL(SubtitleOptions) as subs:
                subs.download([f"https://www.youtube.com/watch?v={VideoID}"])

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
                    subprocess.call(f'ffmpeg -i "{input}" -vn -f mp3 "{TempPath} (audio).mp3"')

            AudioOnlyPath = f"{TempPath} (audio).mp3"

            # Finding downloaded video file
            for ext in VideoTypes:
                if os.path.exists(f"{TempPath} (video).{ext}"):
                    VideoOnlyPath = f"{TempPath} (video).{ext}"

            # Combines audio and video into one file
            subprocess.call(f'ffmpeg -i "{VideoOnlyPath}" -i "{AudioOnlyPath}"' +
                    f' -metadata title="{video["video_title"]}"' +
                    f' -metadata author="{video["channel_name"]}"' +
                    f' -metadata description="{video["video_description"]}"' +
                    f' -metadata year={video["video_release_date"]}' +
                    f' -codec copy "{OutputPath}.mp4"')

            # Delete audio and video only files.
            files = os.listdir(f"{os.getcwd()}/{TempDir}")

            for file in files:
                if ("(audio)" in file) or ("(video)" in file):
                    if VideoID in file:
                        os.remove(f"{channel}/{file}")
