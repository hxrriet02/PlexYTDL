from __future__ import unicode_literals
from time import strftime

def init():
    with open("latest.log", "w") as file:
        file.write(f"\n        -- Log started at {strftime(f'[%Y-%m-%d %H:%M:%S]')} --         \n\n")

    with open("latest_ffmpeg.log", "w") as file:
        file.write(f"\n        -- Log started at {strftime(f'[%Y-%m-%d %H:%M:%S]')} --         \n\n")

    with open("latest_ytdl.log", "w") as file:
        file.write(f"\n        -- Log started at {strftime(f'[%Y-%m-%d %H:%M:%S]')} --         \n\n")
        
def log(string, BeforeTimestamp = ""): # Need this to work with datetime correctly for an accurate log
    string = strftime(f"{BeforeTimestamp}[%Y-%m-%d %H:%M:%S] {string}")
    print(string)

    with open("latest.log", "a") as file:
        file.write(f"{string} \n")

def end(EndByError = False, error = ""):
    if EndByError == True:
        log(f"Error: {error}")

    with open("latest.log", "a") as file:
        file.write(f"\n        --  Log ended at {strftime(f'[%Y-%m-%d %H:%M:%S]')}  --         \n")

    with open("latest_ffmpeg.log", "a") as file:
        file.write(f"\n        --  Log ended at {strftime(f'[%Y-%m-%d %H:%M:%S]')}  --         \n")

class ffmpeg:
    def log(string):
        time = strftime(f'[%Y-%m-%d %H:%M:%S]')
        string = f"        {time}         \n\n{string}\n\n\n"
        # print(string)

        with open("latest_ffmpeg.log", "a") as file:
            file.write(f"{string} \n")

class ytdl(object):
    def debug(self, msg):
        string = f"{strftime(f'[%Y-%m-%d %H:%M:%S]')} [Debug] {msg}"
        print(string, end="\r")

        # Causes spam whenn downloading
        # with open("latest_ytdl.log", "a") as file:
        #    file.write(f"{string} \n")

    def warning(self, msg):
        string = f"{strftime(f'[%Y-%m-%d %H:%M:%S]')} [Warn]  {msg}"
        print(string)

        with open("latest_ytdl.log", "a") as file:
            file.write(f"{string} \n")

    def error(self, msg):
        string = f"{strftime(f'[%Y-%m-%d %H:%M:%S]')} [Error] {msg}"
        print(string)

        with open("latest_ytdl.log", "a") as file:
            file.write(f"{string} \n")
