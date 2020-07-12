#
#   Sets up the files and first time setup. #
#      Only used when called by main.py     #
#

import easygui, json

defaultSettings = {
"api_key": "",
"output_dir": "",
"temp_dir": "",
"to_download": {
    "channel_ids": [
        ""
    ],
    "channel_usernames": [

    ]
},
"max_videos": 10,
"scan_interval": "12h",
"download_channel_art": True
}

def settings():
    defaultSettings["api_key"] = input("\n  -- Setup --\n\nPlease enter your API key: ")
    print("Please enter the output directory for videos")
    defaultSettings["output_dir"] = easygui.diropenbox()

    while True:
        choice = input("Do you want channel art (banner) to be downloaded? (y/n): ")
        if choice == "y":
            defaultSettings["download_channel_art"] = True
            break
        elif choice == "n":
            defaultSettings["download_channel_art"] = False
            break
        else:
            print("Please enter y or n")

    print("\nHow long between scans for videos? (0 for don't scan)")
    print("     use a number (eg. 1, 2, 12) followed by m, h or d for minutes, hours or days")
    print("     leave black for default: 12 hours between scans (12h)")
    choice = input()
    if choice == "0":
        defaultSettings["scan_interval"] = "12h"
    else:
        defaultSettings["scan_interval"] = choice

    print("\nWhile videos are downloading they are stored in a temporary" +
    "location, leave blank for 'videos/' or change it now")
    defaultSettings["temp_dir"] = input()

    print("\nWhat channel would you like to download using their channel id?")
    print("     example: id of 'https://www.youtube.com/channel/UCdBK94H6oZT2Q7l0-b0xmMg' is 'UCdBK94H6oZT2Q7l0-b0xmMg'")
    print("     add more in settings.json")
    defaultSettings["to_download"]["channel_ids"][0] = input()

    print("\nWhat channel would you like to download using their channel id?")
    print("     example: id of 'https://www.youtube.com/user/LinusTechTips' is 'LinusTechTips'")
    print("     add more in settings.json")
    defaultSettings["to_download"]["channel_usernames"][0] = input()

    with open("settings.json", "w") as file:
        json.dump(defaultSettings, file, sort_keys=True, indent=4,
                        separators=(',', ': '))
