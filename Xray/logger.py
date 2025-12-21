import logging as _logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "xray.log")

# Basic logging configuration: writes to file and stdout
_logging.basicConfig(
    level=_logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[_logging.FileHandler(LOG_FILE), _logging.StreamHandler()],
)

# Export the configured logging object under the name `logging` so other
# modules can do `from Xray.logger import logging` and call `logging.info(...)`.
logging = _logging
