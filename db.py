# db.py

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#  Connection String (MongoDB Atlas)
uri = "mongodb+srv://shikha:shikha@clustermy.9mszedl.mongodb.net/learning_db?retryWrites=true&w=majority&appName=ClusterMy"

#  Create Client
client = MongoClient(uri, server_api=ServerApi('1'))

#  Database & Collection
db = client["learning_db"]
collection = db["students"]

#  Test Connection
def test_connection():
    try:
        client.admin.command('ping')
        print(" Connected to MongoDB Atlas!")
    except Exception as e:
        print(" Connection Error:", e)

# Insert Data
def insert_data(student, score):
    try:
        data = {
            "hours_studied": int(student['Hours Studied']),
            "previous_scores": int(student['Previous Scores']),
            "extracurricular": int(student['Extracurricular Activities']),
            "sleep_hours": int(student['Sleep Hours']),
            "sample_papers": int(student['Sample Question Papers Practiced']),
            "performance": float(score)
        }

        collection.insert_one(data)

    except Exception as e:
        print(" Insert Error:", e)

# 🔹 Fetch All Data (for dashboard)
def get_all_data():
    try:
        return list(collection.find({}, {"_id": 0}))
    except:
        return []