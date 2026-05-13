import sys 
import os 
import numpy as np
import pandas as pd
from pymongo import MongoClient
from zipfile import Path
from src.constant import*
from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils
from dataclasses import dataclass 


@dataclass
class DataIngestionConfig:
  artifact_folder:str = os.path.join(artifact_folder)
  

class DataIngestion:
  def __init__(self):
    self.data_ingestion_config = DataIngestionConfig()
    self.utils = MainUtils()
    
  def export_collection_as_dataframe(self,collection_name, db_name):
    try:
      #connecting to the MongoDB database using the MongoClient class from the pymongo library. The MONGO_DB_URL variable contains the connection string for the MongoDB database, which includes the username, password, and host information needed to establish a connection.
      mongo_client = MongoClient(MONGO_DB_URL)
      
      collection = mongo_client[db_name][collection_name]
      
      df= pd.DataFrame(list(collection.find())) # The find() method is used to retrieve all documents from the specified collection in the MongoDB database. The result is a cursor object that can be iterated over to access each document. By converting the cursor to a list and then creating a DataFrame from it, we can easily manipulate and analyze the data using pandas.
      
      if "_id" in df.columns.to_list():
        df = df.drop(columns = ["_id"],axis=1)
      
      df.replace({"na":np.nan},inplace=True)  # replacing missing values with np.nan
      
      return df
    except Exception as e:
      raise CustomException(e, sys)  # ( e )is the error, and ( sys ) is the error details 
  
  def export_data_into_feature_store_file_path(self) -> pd.DataFrame:
    try:
      logging.info(f"Exporting data from MongoDB")
      raw_file_path = self.data_ingestion_config.artifact_folder  # os.path.join(self.data_ingestion_config.artifact_folder, "raw_data.csv") is the file path where the raw data will be saved. It combines the artifact folder path with the file name "raw_data.csv" to create the complete file path for storing the raw data.
      
      os.makedirs(raw_file_path, exist_ok=True) # even if the folder already exists , it will not throw an error
      
      sensor_data = self.export_collection_as_dataframe(
        collection_name = MONGO_COLLECTION_NAME,
        db_name = MONGO_DATABASE_NAME
      )
      
      logging.info(f"Saving exported data into feature store file path:{raw_file_path}")
      
      feature_store_file_path = os.path.join(raw_file_path,'wafer_fault.csv')
      
      sensor_data.to_csv(feature_store_file_path, index=False)  # saving the data in csv format and index = False means that the index column will not be included in the output CSV file.
      
      return feature_store_file_path
    except Exception as e:
      raise CustomException(e, sys)
  
  # this method will be called from the main.py file to start the data ingestion process. It will call the export_data_into_feature_store_file_path method to get the data from MongoDB and save it in the feature store file path. Finally, it will return the feature store file path where the data is saved.  
  def initiate_data_ingestion(self) -> Path:
    logging.info("Entered the initiate_data_ingestion method of data_ingestion class")
    
    try:
      feature_store_file_path = self.export_data_into_feature_store_file_path()
      
      logging.info("got the data from MongoDB")
      
      logging.info("exited initiate_data_ingestion method of data_ingestion class")
      
      return feature_store_file_path
    except Exception as e:
      raise CustomException(e, sys) from e
  # this method will be called from the main.py file to start the data ingestion process. It will call the export_data_into_feature_store_file_path method to get the data from MongoDB and save it in the feature store file path. Finally, it will return the feature store file path where the data is saved.