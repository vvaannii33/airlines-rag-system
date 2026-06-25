import logging
import os

# create logs folder if not exists
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,

    format= "%(asctime)s | %(levelname)s |%(filename)s:%(lineno)d | %(message)s",

    handlers=[
        logging.FileHandler("logs/app.log",mode="w"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)