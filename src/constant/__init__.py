import os 


AWS_S3_BUCKET_NAME = "wafer-fault"
MONGO_DATABASE_NAME ="koushik_wafer_fault"
MONGO_COLLECTION_NAME= "waferfault"

TARGET_COLUMN = 'quality'
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

MODEL_FILE_NAME ="model"
MODEL_FILE_EXTENSION =".pkl"