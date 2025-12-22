import os
import sys
import types
from pathlib import Path
from PIL import Image
import pytest

# Create lightweight stubs for torch/torchvision to avoid importing heavy C extensions
# during collection on Windows machines where torch DLLs may fail to load.
if 'torch' not in sys.modules:
    torch_stub = types.SimpleNamespace()
    # minimal cuda/device implementations used in constants
    torch_stub.cuda = types.SimpleNamespace(is_available=lambda: False)
    torch_stub.device = lambda *a, **k: 'cpu'
    sys.modules['torch'] = torch_stub
    # Provide minimal structure for torch.utils.data
    torch_utils = types.SimpleNamespace()
    sys.modules['torch.utils'] = torch_utils
    class SimpleDataset(list):
        pass
    class SimpleDataLoader:
        def __init__(self, dataset, **kwargs):
            self.dataset = dataset
        def __len__(self):
            return len(self.dataset)
    sys.modules['torch.utils.data'] = types.SimpleNamespace(DataLoader=SimpleDataLoader, Dataset=SimpleDataset)
    # Also provide the dataloader submodule path used in some imports
    sys.modules['torch.utils.data.dataloader'] = types.SimpleNamespace(DataLoader=SimpleDataLoader)

if 'torchvision' not in sys.modules:
    # Provide minimal torchvision.transforms and datasets.ImageFolder
    # Pickle-friendly Compose defined at module level so joblib can serialize it during tests
    class Compose:
        def __init__(self, lst):
            self.transforms = lst
        def __call__(self, x):
            return x

    torchvision = types.SimpleNamespace()
    torchvision.transforms = types.SimpleNamespace(Compose=Compose, Resize=lambda *a, **k: None,
                                                   CenterCrop=lambda *a, **k: None, ColorJitter=lambda *a, **k: None,
                                                   RandomHorizontalFlip=lambda *a, **k: None, RandomRotation=lambda *a, **k: None,
                                                   ToTensor=lambda *a, **k: None, Normalize=lambda *a, **k: None)

    class ImageFolderStub(list):
        def __init__(self, root, transform=None):
            self.root = root
            self.transform = transform
            # collect files
            items = []
            for class_name in os.listdir(root):
                class_dir = os.path.join(root, class_name)
                if os.path.isdir(class_dir):
                    for fname in os.listdir(class_dir):
                        items.append((os.path.join(class_dir, fname), class_name))
            super().__init__(items)
        def __len__(self):
            return list.__len__(self)

    torchvision.datasets = types.SimpleNamespace(ImageFolder=ImageFolderStub)
    sys.modules['torchvision'] = torchvision
    sys.modules['torchvision.transforms'] = torchvision.transforms
    sys.modules['torchvision.datasets'] = torchvision.datasets

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

    # Using lightweight stub DataLoader above: ensure dataset length matches files count
    assert len(train_loader.dataset) == 2
    assert len(test_loader.dataset) == 2

    artifact = dt.initiate_data_transformation()

    assert artifact.train_transform_file_path == config.train_transforms_file
    assert artifact.test_transform_file_path == config.test_transforms_file
    assert os.path.exists(artifact.train_transform_file_path)
    assert os.path.exists(artifact.test_transform_file_path)
