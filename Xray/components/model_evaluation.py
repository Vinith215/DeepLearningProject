import sys
from Xray.exception import XRayException
from Xray.logger import logging
from Xray.entity.config_entity import ModelEvaluationConfig
from Xray.entity.artifact_entity import ModelEvaluationArtifact, ModelTrainerArtifact, DataTransformationArtifact


class ModelEvaluation:
    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_evaluation_config: ModelEvaluationConfig,
        model_trainer_artifact: ModelTrainerArtifact,
    ):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_evaluation_config = model_evaluation_config
        self.model_trainer_artifact = model_trainer_artifact

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        logging.info("Entered the initiate_model_evaluation method of ModelEvaluation class")
        try:
            # Stub: accept whatever model is provided
            logging.info("Model evaluation is a stub — accepting model by default")
            return ModelEvaluationArtifact(is_model_accepted=True)

        except Exception as e:
            raise XRayException(e, sys)
