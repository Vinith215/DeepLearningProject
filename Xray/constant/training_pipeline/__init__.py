from datetime import datetime
from typing import List

import torch

TIMESTAMP: datetime= datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

ARTIFACT_DIR: str = "artifacts"

BUCKET_NAME: str = "xraylungimgs"

S3_DATA_FOLDER: str = "data"

CLASS_LABEL_1: str= "Normal"

CLASS_LABEL_2: str= "Pneumonia"

