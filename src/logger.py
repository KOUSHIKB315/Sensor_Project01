import logging  
import os    # For file handling
from datetime import datetime  # For timestamping log entries
LOG_FILE = f"{datetime.now().strftime("%m_%d_%Y_%H_%M_%s")}.log" # Log file name with timestamp

logs_path = os.path.join(os.getcwd(),"logs",LOG_FILE) # joining current working directory with logs folder and log file name to make the complete path for log file

os.makedirs(logs_path, exist_ok=True) # Create the logs directory if it doesn't exist, exist_ok=True prevents an error if the directory already exists

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE) # Complete path for the log file

logging.basicConfig(
  filename= LOG_FILE_PATH,
  format ="[%(asctime)s]%(lineno)d %(name)s - %(levelname)s - %(message)s",
  level = logging.INFO  # Set the logging level to INFO, which means that all messages with a severity level of INFO and above will be logged. levels include DEBUG, INFO, WARNING, ERROR, and CRITICAL, with DEBUG being the lowest level and CRITICAL being the highest. By setting the level to INFO, i will capture all messages that are INFO, WARNING, ERROR, and CRITICAL, but not DEBUG messages.
  
)