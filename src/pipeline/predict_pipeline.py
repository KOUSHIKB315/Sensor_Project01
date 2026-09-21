import shutil # i import shutil to copy files and directories, simply because i want to copy the model.pkl file from the artifacts folder to the deployment folder.
import os 
import sys 
import pandas as pd 
import pickle 
from src.logger import logging 
from src.exception import CustomException 
from flask import request # i import request from flask to get the data from the user in the form of json, so that i can convert it into a dataframe and then pass it to the model for prediction. 
from src.constant import *
from src.utils.main_utils import MainUtils 
from dataclasses import dataclass 

# MAKING PREDICTION PIPELINE CLASS >> this class defines the configuration for the prediction pipeline, including paths for models, preprocessors, and prediction outputs
# ARTTRIBUTES >> 
  # prediction_output_dirname : directory where the prediction results will be saved 
  # prediction_file_name : name of the file where the prediction will be stored 
  # model_file_path : path to the serialized machine learning model(model.pkl)
  # preprocessor_path : path to the preprocessor used for data transformation 
  # prediction_file_path : path where the prediction file will saved 
  
@dataclass
class PredictionPipelineConfig:
  prediction_output_dirname: str = "predictions"
  prediction_file_name : str = "prediction_file.csv"
  model_file_path : str = os.path.join(artifact_folder, 'model.pkl')
  preprocessor_path : str = os.path.join(artifact_folder, 'preprocessor.pkl')
  prediction_file_path : str = os.path.join(prediction_output_dirname, prediction_file_name) # (dirname , filename) this will make the location where the file will be stored 

# MAKING PREDICTION PIPELINE CLASS >> this is the main class that handles the prediction process
# ATTRIBUTES >> 
  # purpose : initializes the PredictionPipeline class 
  # request : the incoming request containing the input data (likely an uploaded CSV file)
  # utils : instance of MainUtils for loading models , preprocessors, and other utility functions
  # prediction_pipeline_config : configuration object containing paths for files and directories 
  
class PredictionPipeline:
  def __init__(self, request: request):
    self.request = request
    self.utils = MainUtils()
    self.prediction_pipeline_config = PredictionPipelineConfig()
    
    # creating a method called ( save_input_files ) , it will save the input file uploaded by the user into a directory for prediction artifacts 
      # steps >>
      # 1. create a directory called (prediction_artifacts), if it does not exist 
      # 2. extract the uploaded file from the request and save it to the directory 
      # Return : path to the saved input CSV file 
      
  def save_input_files(self)->str:
    try:
      pred_file_input_dir = "prediction_artifacts"
      os.makedirs(pred_file_input_dir, exist_ok=True)
      
      input_csv_file = self.request.files['file']
      pred_file_path = os.path.join(pred_file_input_dir, input_csv_file.filename)
      
      input_csv_file.save(pred_file_path)
      
      return pred_file_path
    except Exception as e:
      raise CustomException(e,sys)
    
  # MAKING (predict) method >> 
  # uses the pre-trained model and preprocessor to make predictions on the input features
  # STEPS >>
  # 1. load the trained model and preprocessor using MainUtils.load_objects()
  # 2. apply the preprocessor to transform the input features
  # 3. use the model to predict the output based on the transformed features
  # RETURN : the predicted values 
  
  def predict(self, features):
    try:
      model = self.utils.load_object(self.prediction_pipeline_config.model_file_path)
      preprocessor = self.utils.load_object(file_path = self.prediction_pipeline_config.preprocessor_path) 
      
      transformed_x = preprocessor.transform(features)
      preds = model.predict(transformed_x)
      
      return preds
    except Exception as e:
      raise CustomException(e,sys)
    
  # MAKING (get_predicted_dataframe) method >> this method reads the input CSV file , makes predictions ,and adds a new column for the predictions
  # STEPS : 
  # 1. read the input data from the csv file 
  # 2. drop any unwanted columns (eg. Unnamed:0)
  # 3. call the predict() method to get productions for the input data 
  # 4. map the prediction values ( 0 and 1 ) to human-readable lables( 'bad' and 'good')
  # 5. save the resulting DataFrame with the predictions to a CSV file 
  
  # output : the CSV is saved to the specific path , and predictions are logged 
  
  def get_predicted_dataframe(self, input_dataframe_path: pd.DataFrame):
    try:
      prediction_column_name :str = TARGET_COLUMN 
      input_dataframe:pd.DataFrame = pd.read_csv(input_dataframe_path) 
      
      input_dataframe = input_dataframe.drop(columns = "Unnamed: 0") if "Unnamed: 0" in input_dataframe.columns else input_dataframe
      
      predictions = self.predict(input_dataframe)
      input_dataframe[prediction_column_name] = [pred for pred in predictions] 
      
      target_column_mapping = {0:'bad', 1:'good'}
      input_dataframe[prediction_column_name] = input_dataframe[prediction_column_name].map(target_column_mapping) 
      
      os.makedirs(self.prediction_pipeline_config.prediction_output_dirname, exist_ok=True)
      
      input_dataframe.to_csv(self.prediction_pipeline_config.prediction_file_path, index=False)
      
      logging.info("predictions completed")
    except Exception as e:
      raise CustomException(e,sys) from e
    
  # MAKING (run_pipeline) method >> it orchestrates the prediction process by running the entire pipeline 
  # STEPS : 
  # 1. calls save_input_files() to save the input files
  # 2. calls get_predicted_dataframe() to generate predictions and save them to a file
  # RETURN : returns the configuration object, which contains the file path used in the prediction process 
  
  def run_pipeline(self):
    try:
      input_csv_path = self.save_input_files()
      self.get_predicted_dataframe(input_csv_path)
      
      return self.prediction_pipeline_config
    except Exception as e:
      raise CustomException(e,sys) 