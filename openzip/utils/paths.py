import os

# directories
APP_BASE_DIR = os.path.join(os.getcwd().split("OpenZip")[0], "OpenZip")
DATA_DIR = os.path.join(APP_BASE_DIR, "data")
ASSETS_DIR = os.path.join(DATA_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
TEMP_DIR = os.path.join(DATA_DIR, "temp")
LOGS_DIR = os.path.join(DATA_DIR, "logs")
ICONS_DIR = os.path.join(IMAGES_DIR, "icons")

# icons
ONLINE16_ICON_PATH = os.path.join(ICONS_DIR, "online_16x16.png")
OFFLINE16_ICON_PATH = os.path.join(ICONS_DIR, "offline_16x16.png")

CLIENT48_ICON_PATH = os.path.join(ICONS_DIR, "client_48x48.png")
SERVER48_ICON_PATH = os.path.join(ICONS_DIR, "server_48x48.png")

CLIENT64_ICON_PATH = os.path.join(ICONS_DIR, "client_64x64.png")
SERVER64_ICON_PATH = os.path.join(ICONS_DIR, "server_64x64.png")
LOG64_ICON_PATH = os.path.join(ICONS_DIR, "log_64x64.png")

CLIENT128_ICON_PATH = os.path.join(ICONS_DIR, "client_128x128.png")
SERVER128_ICON_PATH = os.path.join(ICONS_DIR, "server_128x128.png")

CLIENT256_ICON_PATH = os.path.join(ICONS_DIR, "client_256x256.png")
SERVER256_ICON_PATH = os.path.join(ICONS_DIR, "server_256x256.png")
LOADING256_GIF_PATH = os.path.join(ICONS_DIR, "loading_256x256.gif")


if __name__ == "__main__":
    for value in dir():
        if isinstance(eval(value), str) and value.isupper():
            print(f"[{'V' if os.path.exists(eval(value)) else 'X'}] {value}: {eval(value)}")
