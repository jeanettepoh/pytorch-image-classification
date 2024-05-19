import os
import sys
import logging

from src.constant.training_pipeline import TIMESTAMP


# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_dir, exist_ok=True)


# Define log filename with timestamp
log_filename: str = f"{TIMESTAMP}.log"
log_filepath = os.path.join(logs_dir, log_filename)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s: %(module)s: %(message)s]",
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("ImageClassifierLogger")