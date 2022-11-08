import logging
import os

from openzip.utils.paths import LOGS_DIR
from openzip.utils.constants import LOG_FILENAME


logging.basicConfig(filename=os.path.join(LOGS_DIR, LOG_FILENAME),
                    filemode="a",
                    format="%(levelname)s - %(module)s on line %(lineno)d -- %(message)s",
                    level=logging.DEBUG)
