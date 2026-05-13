from pymongo.mongo_client import MongoClient
import pandas as pd
import json

# URL

url = "mongodb+srv://koushikbandyopadhyay3152003:KoushikCST07@waferfaultcluster.rl2cipw.mongodb.net/?appName=waferfaultcluster"

# Create a new Client and Connect to server : 

client = MongoClient(url)

# Create Database name and Collection name : 

DATABASE_NAME = 'pwskills'
COLLECTION_NAME = 'wafer_fault'

df= pd.read_csv(r"D:\Sensor_Project\notebooks\wafer_23012020_041211.csv")

df = df.drop('Unnamed: 0', axis=1)

# Converting the df into JSON so that i can upload it to MongoDB : 

json_record = list(json.loads(df.T.to_json()).values())

type(json_record)

# now i shall dump the data inside the MongoDB Database :

client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)

