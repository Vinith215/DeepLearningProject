from dataclasses import dataclass
from torch.utils.data.dataloader import DataLoader

@dataclass 
class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str
    
@dataclass
class DataTransformationArtifact:
    transformed_train_object: DataLoader

    transformed_test_object: DataLoader

    train_transform_file_path: str

    test_transform_file_path: str


@dataclass
class ModelTrainerArtifact:
    """Minimal artifact produced by the (stub) model trainer."""

    model_path: str = ""


@dataclass
class ModelEvaluationArtifact:
    """Minimal artifact produced by the (stub) model evaluation."""

    is_model_accepted: bool = True


@dataclass
class ModelPusherArtifact:
    """Minimal artifact produced by the (stub) model pusher."""

    pusher_model_dir: str = ""
