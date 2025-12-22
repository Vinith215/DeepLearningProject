import os
from pathlib import Path
from PIL import Image
import pytest

from Xray.components.data_transformation import DataTransformation
from Xray.entity.config_entity import DataTransformationConfig
from Xray.entity.artifact_entity import DataIngestionArtifact
from Xray.constant.training_pipeline import TRAIN_TRANSFORMS_FILE, TEST_TRANSFORMS_FILE


def create_dummy_image(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (10, 10), color=(155, 0, 0))
    img.save(path)


def test_data_transformation_end_to_end(tmp_path):
    # Create fake train/test folders with class subfolders
    train_dir = tmp_path / "train"
    test_dir = tmp_path / "test"

    (train_dir / "NORMAL").mkdir(parents=True)
    (train_dir / "PNEUMONIA").mkdir(parents=True)
    (test_dir / "NORMAL").mkdir(parents=True)
    (test_dir / "PNEUMONIA").mkdir(parents=True)

    # Create 2 small images per class
    create_dummy_image(train_dir / "NORMAL" / "img1.jpg")
    create_dummy_image(train_dir / "PNEUMONIA" / "img2.jpg")
    create_dummy_image(test_dir / "NORMAL" / "img3.jpg")
    create_dummy_image(test_dir / "PNEUMONIA" / "img4.jpg")

    # Prepare artifacts and config
    ingestion_artifact = DataIngestionArtifact(
        train_file_path=str(train_dir), test_file_path=str(test_dir)
    )

    config = DataTransformationConfig()
    # Override artifact dir to be inside tmp_path so test is isolated
    config.artifact_dir = str(tmp_path / "artifacts")
    config.train_transforms_file = os.path.join(config.artifact_dir, TRAIN_TRANSFORMS_FILE)
    config.test_transforms_file = os.path.join(config.artifact_dir, TEST_TRANSFORMS_FILE)

    dt = DataTransformation(
        data_transformation_config=config, data_ingestion_artifact=ingestion_artifact
    )

    train_tf = dt.transforming_training_data()
    test_tf = dt.transforming_testing_data()

    assert train_tf is not None
    assert test_tf is not None

    train_loader, test_loader = dt.data_loader(train_tf, test_tf)

    # Default batch_size in constants is small; ensure loaders return dataset with length 2
    assert len(train_loader.dataset) == 2
    assert len(test_loader.dataset) == 2

    artifact = dt.initiate_data_transformation()

    assert artifact.train_transform_file_path == config.train_transforms_file
    assert artifact.test_transform_file_path == config.test_transforms_file
    assert os.path.exists(artifact.train_transform_file_path)
    assert os.path.exists(artifact.test_transform_file_path)
