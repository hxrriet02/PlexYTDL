#                                                    #
#    Will be used for getting info about channels    #
#             and save it to videos.json             #
#                                                    #

import json, urllib, re, logger

videoJSON = {
    "channel_name": "",
    "channel_id": "",
    "video_title": "",
    "video": {
        "description":"",
        "release_date":"",
        "thumbnail_url":"",
        "title":"",
        "id":""
    },
    "progress": {
        "downloaded_video_only": False,
        "downloaded_audio_only": False,
        "downloaded_final": False,
        "dir_video_only": "",
        "dir_audio_only": "",
        "dir_final": ""
    },
    "subtitles": [

    ]
}

VideoIdsInJson = [ ]
VideoFinalDirs = [ ]

def start():
    # Get channels from JSON file
    logger.log("Getting channels from settings JSON")
    with open("channels.json", "r") as file:
        with open("settings.json", "r") as fileSettings:
            rawJson = json.loads(file.read())
            settingsJson = json.loads(fileSettings.read())

            if file.read == "[]":
                ScanChannels(settingsJson, True)
            else:
                ScanChannels(settingsJson, False)

def ScanChannels(settings, FileEmpty):
    with open("videos.json", "r") as f:
        array = json.loads(f.read())
        for video in array:
            # Add video ids from current 'videos.json' to then check later
            VideoIdsInJson.append(video["video"]["id"])
            # Check if video has already been downloaded
            # VideoFinalDirs.append(video["progress"]["dir_final"])

    # Clears the video.json file (would be better to keep data and just append
    #                                   to it but thats a task for another day)
    # with open("videos.json", "w") as f:
    #    f.write("[]")

    # For each channel get playlist of uploads, then get list of videos
    logger.log("Getting playlist IDs for channels using IDs")
    if len(settings["to_download"]["channel_ids"]) > 0:
        for ChannelID in settings["to_download"]["channel_ids"]:
            # Gets playlist ID for channel uploads
            ChannelURL = f'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&key={settings["api_key"]}&id={ChannelID}'

            with urllib.request.urlopen(ChannelURL) as request:
                PlaylistID = json.load(request)["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
                UpdateVideoFile(settings["api_key"], settings["max_videos"], PlaylistID, settings["exceptions"], settings["output_dir"])

    # For usernames
    logger.log("Getting playlist IDs for channels using usernames")
    if len(settings["to_download"]["channel_usernames"]) > 0:
        for ChannelUser in settings["to_download"]["channel_usernames"]:
            ChannelURL = f'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&key={settings["api_key"]}&forUsername={ChannelUser}'

            with urllib.request.urlopen(ChannelURL) as request:
                PlaylistID = json.load(request)["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
                UpdateVideoFile(settings["api_key"], settings["max_videos"], PlaylistID, settings["exceptions"], settings["output_dir"])

    # For playlist IDs
    logger.log("Getting playlist IDs")
    if len(settings["to_download"]["playlist_ids"]) > 0:
        for playlist in settings["to_download"]["playlist_ids"]:
            UpdateVideoFile(settings["api_key"], settings["max_videos"], playlist, settings["exceptions"], settings["output_dir"])

# Gets videos from playlist ID, then updates the videos.json
def UpdateVideoFile(api_key, max_videos, PlaylistID, exceptions, OutputDir):
    # Gets videos from uploads playlist (up to max_videos in config)
    PlaylistRequestURL = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&key={api_key}&maxResults={max_videos}&playlistId={PlaylistID}'

    # Gets the JSON from the request
    logger.log("  - Getting JSON from playlist ID")
    with urllib.request.urlopen(PlaylistRequestURL) as request:
        playlist = json.load(request)

    # Gets current JSON
    with open("videos.json") as file:
        VideoFile = json.loads(file.read())

    # Loop for each video in the playlist
    logger.log(f"Adding videos for playlist with ID: {PlaylistID}", "\n")
    for video in playlist["items"]:
        if video["snippet"]["resourceId"]["videoId"] not in VideoIdsInJson:
            videoJSON["channel_name"] = video["snippet"]["channelTitle"]
            videoJSON["channel_id"] = video["snippet"]["channelId"]
            videoJSON["video"]["title"] = video["snippet"]["title"]
            videoJSON["video"]["id"] = video["snippet"]["resourceId"]["videoId"]
            videoJSON["video"]["description"] = video["snippet"]["description"]
            videoJSON["video"]["release_date"] = video["snippet"]["publishedAt"].split("T")[0]
            videoJSON["progress"]["dir_final"] = OutputDir + re.sub(r"\W+", " ", videoJSON["video"]["title"])

            # Could change this to use the final index of the "thumbnails" section to avoid using try-catch.
            try:
                videoJSON["video"]["thumbnail_url"] = video["snippet"]["thumbnails"]["maxres"]["url"]
            except KeyError:
                videoJSON["video"]["thumbnail_url"] = video["snippet"]["thumbnails"]["high"]["url"]

            logger.log("  - Adding '" + videoJSON["channel_name"] + "' - '" + videoJSON["video"]["title"] + "'")

            # Check for exceptions
            logger.log("      - Checking for exceptions")
            for exception in exceptions:
                if exception["keyword"] in videoJSON["video"]["title"]:
                    logger.log("      - Exception found, replacing '" + videoJSON["channel_name"] + "' for '" + exception["new_channel_name"] + "'")
                    videoJSON["channel_name"] = exception["new_channel_name"]


            VideoFile.append(videoJSON)

        # Remove the videos that have been downloaded from the 'videos.json' file
        # if re.sub(r"\W+", " ", videoJSON["video"]["title"]) not in os.listdir(f'{OutputDir}/{video["snippet"]["channelTitle"]}'):


    # Appends new video to JSON
    logger.log("  - Adding new videos to the 'videos.json'")
    with open("videos.json", "w") as file:
        json.dump(VideoFile, file, sort_keys=True, indent=4,
                        separators=(',', ': '))
