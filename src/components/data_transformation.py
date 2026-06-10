import sys 
import os
import pandas as pd  
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer 
from sklearn.preprocessing import RobustScaler, FunctionTransformer
from sklearn.pipeline import Pipeline 
from sklearn.preprocessing import StandardScaler

from src.constant import*
from src.exception import CustomException 
from src.logger import Logging 
from src.utils.main_utils import MainUtils
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
  # this class is responsible for storing the file paths for the transformed data and the preprocessor object in the artifact folder
  artifact_dir = os.path.join(artifact_folder)
  transformd_train_file_path = os.path.join(artifact_dir,'train.npy')
  transformd_test_file_path = os.path.join(artifact_dir,'test.npy')
  transformd_object_file_path = os.path.join(artifact_dir,'preprocessor.pkl') # because i am storing object , so in .pkl format
  
class DataTransformation:
  # this class is responsible for transforming the data and saving the transformed data and the preprocessor object in the artifact folder
  def __init__(self, feature_store_file_path):
    # feature_store_file_path is the file path where the raw data is stored after data ingestion and we will use this file path to read the raw data and then transform it and save the transformed data in the artifact folder
    self.feature_store_file_path = feature_store_file_path
    self.data_transformation_config = DataTransformationConfig()
    self.utils = MainUtils()
    
  @staticmethod
  def get_data(feature_store_file_path:str)->pd.DataFrame:
    # this method is responsible for reading the raw data from the file path and returning it as a pandas dataframe
    try:
      data = pd.read_csv(feature_store_file_path)
      
      data.rename(columns={'Good/Bad':TARGET_COLUMN},inplace=True)
      return data 
    except Exception as e:
      raise CustomException(e,sys)
    
  def get_data_transformer_object(self):
    # this method is responsible for creating the preprocessor object which will be used to transform the data and then we will save this preprocessor object in the artifact folder
    try:
      imputer_step = ('imputer',SimpleImputer(strategy='constant',fill_value=0))
      scaler_step = ('scaler',RobustScaler())
      
      preprocessor = Pipeline(
        steps=[
          imputer_step,
          scaler_step
        ]
      )
      return preprocessor
    except Exception as e:
      raise CustomException(e,sys)
    
  def initiate_data_transformation(self):
    
    logging.info('entered initiated data transformation method of data transformation class')
    
    try:
      dataframe = self.get_data(feature_store_file_path = self.feature_store_file_path)
      
      x = dataframe.drop(columns=TARGET_COLUMN)
      y= np.where(dataframe[TARGET_COLUMN]== -1,0,1) # because in the dataset -1 is for bad and 1 is for good , so we are replacing -1 with 0 and keeping 1 as it is
      
      x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2)
      preprocessor = self.get_data_transformer_object() 
      
      x_train_scaled = preprocessor.fit_transform(x_train)
      x_test_scaled = preprocessor.transform(x_test)
      
      preprocessor_path = self.data_transformation_config.transformd_object_file_path
      os.makedirs(os.path.dirname(preprocessor_path), exist_ok=True)
      
      self.utils.save_object(file_path= preprocessor_path, obj=preprocessor)
      
      train_arr = np.c[x_train_scaled,np.array(y_train)]
      test_arr = np.c[x_test_scaled,np.array(y_test)]
      
      return (train_arr, test_arr, preprocessor_path)
    except Exception as e:
      raise CustomException(e,sys) from e