import sys
from Xray.exception import XRayException
from Xray.logger import logging
from Xray.entity.config_entity import ModelTrainerConfig
from Xray.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact


class ModelTrainer:
    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_config: ModelTrainerConfig,
    ):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        logging.info("Entered the initiate_model_trainer method of ModelTrainer class")
        try:
            # This is a stubbed trainer. Replace with real training logic.
            logging.info("Model training is a stub — skipping actual training")
            return ModelTrainerArtifact(model_path=self.model_trainer_config.model_path)

        except Exception as e:
            raise XRayException(e, sys)
