import os
import sys
import shutil
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi
from src.logger import logger
from src.exception import CustomException
from src.entity.artifact_entity import DataIngestionArtifact
from src.entity.config_entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
    
    def download_raw_data(self) -> str:
        try:
            logger.info("Downloading the raw data from Kaggle")

            # Instantiate the Kaggle API client
            api = KaggleApi()
            api.authenticate()

            # Download dataset to specified directory
            os.makedirs(self.data_ingestion_config.artifact_dir, exist_ok=True)
            dataset_name = self.data_ingestion_config.dataset_name
            api.dataset_download_files(
                dataset_name, 
                path=self.data_ingestion_config.artifact_dir, 
                unzip=True
            )

            # Get the path to the downloaded dataset
            for entry in os.scandir(self.data_ingestion_config.artifact_dir):
                if entry.is_dir():
                    raw_data_path = entry.path
                    break

            logger.info("Raw data path is {}".format(raw_data_path))

            return raw_data_path
        
        except Exception as e:
            raise CustomException(e, sys)
   
        
    def move_raw_data_folders(self, raw_data_path):
        try:
            train_data_folder = os.path.join(raw_data_path, "train")
            test_data_folder = os.path.join(raw_data_path, "test")

            # Move train and test data to artifact dir
            try:
                shutil.move(train_data_folder, self.data_ingestion_config.artifact_dir)
                shutil.move(test_data_folder, self.data_ingestion_config.artifact_dir)
            except shutil.Error:
                logger.info("Train and Test directories already moved")
                pass
            
            os.rmdir(raw_data_path)
        
        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        logger.info("Entered the data ingestion phase")
        try:
            raw_data_path = self.download_raw_data()
            self.move_raw_data_folders(raw_data_path)

            data_ingestion_artifact: DataIngestionArtifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.train_data_path,
                test_file_path=self.data_ingestion_config.test_data_path
            ) 

            logger.info("Completed the data ingestion phase")

            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e, sys)

        
if __name__ == "__main__":
    data_ingestion_config = DataIngestionConfig()
    data_ingestion = DataIngestion(data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()