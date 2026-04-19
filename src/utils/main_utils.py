import sys
from typing import Dict, Tuple
import os 
import pandas as pd  
import pickle
import yaml  # to work with YAML files, which are commonly used for configuration files. It provides functions for parsing and emitting YAML data, making it easier to read and write YAML files in Python applications.
import boto3   # to interact with AWS services, such as S3, DynamoDB, etc. It provides a high-level interface for working with AWS resources and allows developers to easily integrate AWS services into their Python applications.


from src.constant import*
from src.exception import CustomException
from src.logger import logging


class MainUils:
  def __init__(self) ->None:
    pass
  
  def read_yaml_file(self, filename:str) -> dict:
    try:
      with open(filename, "rb") as yaml_file:  #rb stands for read binary mode, which is used to read binary data from a file. This is necessary when working with YAML files, as they may contain binary data that cannot be read in text mode.
        return yaml.safe_load(yaml_file)
      
    except Exception as e:
      raise CustomException(e, sys) from e
    
  
  def read_schema_config_file(self)-> dict:   # it will read the schema.yaml file from mongodb and return the contents as dict
    try:
      schema_config = self.read_yaml_file(os.path.join('config','schema.yaml'))
      
      return schema_config
    
    except Exception as e:
      raise CustomException(e, sys) from e
    
  
  @staticmethod   # static method is a decorator that indicates that the method is a static method, which means it can be called on the class itself without needing an instance of the class. This is useful for utility functions that don't require access to instance-specific data.
  def save_object(file_path:str, obj:object) ->None:
    logging.info("Entered the save_object method of MainUtils class")
    
    try:
      with open(file_path,"wb") as file_obj:  # wb stands for write binary mode, which is used to write binary data to a file. This is necessary when working with pickle files, as they contain binary data that cannot be written in text mode.
        pickle.dump(obj, file_obj)
        
      logging.info("Exited the save_object method of MainUtils class")
      
    except Exception as e:
      raise CustomException(e, sys) from e
    
  @staticmethod
  def load_object(file_path:str)-> object:
    logging.info("Entered the load_object method of MainUtils class")
    
    
    try:
      with open(file_path, "rb") as file_obj:
        obj = pickle.load(file_obj)
        
      logging.info("Exited the load_object method of MainUtils class")
      
      return obj
    except Exception as e:
      raise CustomException(e, sys) from e
    
    
