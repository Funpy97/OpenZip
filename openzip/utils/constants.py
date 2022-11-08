import os

# generic constants
APP_VERSION = "0.1"

# backend constants
MAX_PWD_LEN = 30
MAX_CPU_PROCESSES = os.cpu_count()
MAX_DEFAULT_CLIENTS = 10
DEFAULT_CONNECTION_BUFFER = 8192
SCANNER_THREADS = 10
DEFAULT_SERVER_PORT = 49305
LOG_FILENAME = "openzip.log"

# frontend contants
LIGTH_THEME_NAME = "cosmo"
DARK_THEME_NAME = "darkly"
WIN_GEOMETRY = "1024x800+50+50"
WIN_TITLE = "OpenZip" + APP_VERSION

HOME_NAME = "home"
SERVER_NAME = "server"
CLIENT_NAME = "client"
