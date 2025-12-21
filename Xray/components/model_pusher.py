import sys
from Xray.exception import XRayException
from Xray.logger import logging
from Xray.entity.config_entity import ModelPusherConfig
from Xray.entity.artifact_entity import ModelPusherArtifact


class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig):
        self.model_pusher_config = model_pusher_config

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        logging.info("Entered the initiate_model_pusher method of ModelPusher class")
        try:
            # Stub: create the pusher dir and return artifact
            import os

            os.makedirs(self.model_pusher_config.pusher_dir, exist_ok=True)
            logging.info("Model pusher is a stub — created pusher directory")
            return ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.pusher_dir)

        except Exception as e:
            raise XRayException(e, sys)
