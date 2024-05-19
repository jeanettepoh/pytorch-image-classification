import os
import sys
import joblib
from typing import Tuple

from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from torchvision.datasets import ImageFolder

from src.logger import logger
from src.exception import CustomException
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import (DataIngestionArtifact,
                                        DataTransformationArtifact)


class DataTransformation:
    def __init__(
        self,
        data_transformation_config: DataTransformationConfig,
        data_ingestion_artifact: DataIngestionArtifact
    ):
        self.data_transformation_config = data_transformation_config
        self.data_ingestion_artifact = data_ingestion_artifact


    def transform_training_data(self) -> transforms.Compose:
        logger.info("Transforming the training data...")
        try:
            train_transform: transforms.Compose = transforms.Compose(
                [
                    transforms.Resize(self.data_transformation_config.RESIZE),
                    transforms.CenterCrop(self.data_transformation_config.CENTERCROP),
                    transforms.ColorJitter(
                        **self.data_transformation_config.color_jitter_transforms
                    ),
                    transforms.RandomHorizontalFlip(),
                    transforms.RandomRotation(
                        self.data_transformation_config.RANDOMROTATION
                    ),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        **self.data_transformation_config.normalize_transforms
                    )
                ]
            )

            return train_transform
        
        except Exception as e:
            raise CustomException(e, sys)


    def transform_testing_data(self) -> transforms.Compose:
        logger.info("Transforming the testing data...")
        try:
            test_transform: transforms.Compose = transforms.Compose(
                [
                    transforms.Resize(self.data_transformation_config.RESIZE),
                    transforms.CenterCrop(self.data_transformation_config.CENTERCROP),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        **self.data_transformation_config.normalize_transforms
                    )
                ]
            )

            return test_transform
        
        except Exception as e:
            raise CustomException(e, sys)


    def create_data_loader(
        self, 
        train_transform: transforms.Compose, 
        test_transform: transforms.Compose
    ) -> Tuple[DataLoader, DataLoader]:
        
        try:
            logger.info("Creating dataloaders for training and testing data")

            train_data: Dataset = ImageFolder(
                self.data_ingestion_artifact.train_file_path,
                transform=train_transform
            )

            test_data: Dataset = ImageFolder(
                self.data_ingestion_artifact.test_file_path,
                transform=test_transform
            )

            train_loader: DataLoader = DataLoader(
                train_data, **self.data_transformation_config.data_loader_params
            )

            test_loader: DataLoader = DataLoader(
                test_data, **self.data_transformation_config.data_loader_params
            )

            logger.info("Created dataloaders")

            return train_loader, test_loader

        except Exception as e:
            raise CustomException(e, sys)
        
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logger.info("Entered the data transformation phase")
            os.makedirs(self.data_transformation_config.artifact_dir, exist_ok=True)

            train_transform: transforms.Compose = self.transform_training_data()
            test_transform: transforms.Compose = self.transform_testing_data()

            joblib.dump(
                train_transform, self.data_transformation_config.train_transforms_file
            )

            joblib.dump(
                test_transform, self.data_transformation_config.test_transforms_file
            )

            train_loader, test_loader = self.create_data_loader(
                train_transform = train_transform, test_transform = test_transform
            )

            data_transformation_artifact: DataTransformationArtifact = DataTransformationArtifact(
                transformed_train_object=train_loader,
                transformed_test_object=test_loader,
                train_transform_file_path=self.data_transformation_config.train_transforms_file,
                test_transform_file_path=self.data_transformation_config.test_transforms_file
            )

            logger.info("Completed the data transformation phase")

            return data_transformation_artifact
        
        except Exception as e:
            raise CustomException(e, sys)
        

if __name__ == "__main__":
    from src.components.data_ingestion import DataIngestion
    from src.entity.config_entity import DataIngestionConfig

    data_ingestion_config = DataIngestionConfig()
    data_ingestion = DataIngestion(data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

    data_transformation_config = DataTransformationConfig()
    data_transformation = DataTransformation(data_transformation_config, data_ingestion_artifact)
    data_ingestion_artifact = data_transformation.initiate_data_transformation()
