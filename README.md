# Plex YouTube Downloader (YTDL)

A simple YouTube downloader that works with Plex's local media agent.

## But why?

I have very slow internet so I can only watch 1080p30 or 720p60 content. So, if I want to watch anything at its full resolution I either get buffering or have to go to a lower resolution. This means I can let the downloader get the latest videos overnight then watch the videos in 4k or whatever resolution I want.

## Setup

Run `main.py` and follow the setup process. You will need a YouTube API Key (v3) for the setup. If you don't have one already, follow this guide to get one: https://www.slickremix.com/docs/get-api-key-for-youtube/

Currently, the time between scans does not work, but it is on my to-do list.

From there, if you want to download more than one YouTube channel's videos, just go to `settings.json` and add to the `channel_ids` list.

## After Setup

After you've set up the program, each time you want to download videos, just run `main.py`.

## Exceptions

If you would like some videos to be in a different folder to those of the main channel, this is where exceptions come in. For example, LinusTechTips have "WAN Show" videos and they specify this with `- WAN Show` at the end. So, the exceptions will search for any video containing `WAN Show` and put it in a new folder, in my case `The WAN Show`.

#### So, how do you set one up?
In settings there is a section that says, this is the example from above.
```
"exceptions": [
  {
    "keyword": "WAN Show",
    "new_channel_name": "The WAN Show"
  }
]
```
You can copy, or replace this template by adding a ',' after the '}' and adding "keyword" and "new_channel_name" again.


## Future Plans

- [x] Add temp video location
- [x] Separate file for scanning
- [x] JSON file for settings configuration
- [x] JSON file for video information
- [x] Option for subtitles
- [x] Remove the need for a plex agent and just rely on metadata.
- [ ] Option to automatically download channel art
- [ ] Don't delete `video.json` each time scanning is triggered, only append to it
- [ ] Auto scan after set duration.
- [ ] Add time for downloading (such as night only)
