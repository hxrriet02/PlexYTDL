#                                                    #
#    Will be used for getting info about channels    #
#             and save it to videos.json             #
#                                                    #

import json, urllib

videoJSON = {
    "channel_name": "",
    "channel_id":"",
    "video_title":"",
    "video_id":"",
    "video_description":"",
    "video_thumbnail_url":"",
    "video_release_date":""
}

#     "downloaded_video": False,
#     "download_video_started": False,
#     "downloaded_thumbnail": False
# }

def start():
    # Get channels from JSON file
    with open("channels.json", "r") as file:
        with open("settings.json", "r") as fileSettings:
            rawJson = json.loads(file.read())
            settingsJson = json.loads(fileSettings.read())

            if file.read == "[]":
                ScanChannels(settingsJson, True)
            else:
                ScanChannels(settingsJson, False)

def ScanChannels(settings, FileEmpty):
    # Clears the video.json file (would be better to keep data and just append
    #                                   to it but thats a task for another day)
    with open("videos.json", "w") as f:
        f.write("[]")

    # For each channel get playlist of uploads, then get list of videos
    for ChannelID in settings["to_download"]["channel_ids"]:
        # Gets playlist ID for channel uploads
        ChannelURL = f'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&key={settings["api_key"]}&id={ChannelID}'

        with urllib.request.urlopen(ChannelURL) as request:
            PlaylistID = json.load(request)["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            UpdateVideoFile(settings["api_key"], settings["max_videos"], PlaylistID)

    #For usernames
    for ChannelUser in settings["to_download"]["channel_usernames"]:
        ChannelURL = f'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&key={settings["api_key"]}&forUsername={ChannelUser}'

        with urllib.request.urlopen(ChannelURL) as request:
            PlaylistID = json.load(request)["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            UpdateVideoFile(settings["api_key"], settings["max_videos"], PlaylistID)

# Gets videos from playlist ID, then updates the videos.json
def UpdateVideoFile(api_key, max_videos, PlaylistID):
    # Gets videos from uploads playlist (up to max_videos in config)
    PlaylistRequestURL = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&key={api_key}&maxResults={max_videos}&playlistId={PlaylistID}'

    # Gets the JSON from the request
    with urllib.request.urlopen(PlaylistRequestURL) as request:
        playlist = json.load(request)

    # Loop for each video in the playlist
    for video in playlist["items"]:
        currentVideoJSON = videoJSON
        videoJSON["channel_name"] = video["snippet"]["channelTitle"]
        videoJSON["channel_id"] = video["snippet"]["channelId"]
        videoJSON["video_title"] = video["snippet"]["title"]
        videoJSON["video_id"] = video["snippet"]["resourceId"]["videoId"]
        videoJSON["video_description"] = video["snippet"]["description"]
        videoJSON["video_release_date"] = video["snippet"]["publishedAt"].split("T")[0]

        # Could change this to use the final index of the "thumbnails" section to avoid using try-catch.
        try:
            videoJSON["video_thumbnail_url"] = video["snippet"]["thumbnails"]["maxres"]["url"]
        except KeyError:
            videoJSON["video_thumbnail_url"] = video["snippet"]["thumbnails"]["high"]["url"]

        # Gets current JSON
        with open("videos.json") as file:
            VideoFile = json.loads(file.read())
            VideoFile.append(videoJSON)

        # Appends new video to JSON
        with open("videos.json", "w") as file:
            json.dump(VideoFile, file, sort_keys=True, indent=4,
                            separators=(',', ': '))
