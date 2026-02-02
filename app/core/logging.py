import logging
from pathlib import Path

LOG_FILE_PATH = Path(__file__).parent.parent.joinpath("logs").joinpath("app.log")

logging.basicConfig(
    filename=str(LOG_FILE_PATH),
    level=logging.INFO,
    format="[%(asctime)s][%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


logger = logging.getLogger(__name__)
