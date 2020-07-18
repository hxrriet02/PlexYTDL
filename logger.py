from time import strftime

def init():
    with open("latest.log", "w") as file:
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
