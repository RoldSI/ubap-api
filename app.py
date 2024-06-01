from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()

app = Flask(__name__)

# MongoDB Atlas connection string
MONGO_URL = os.getenv('MONGO_URL')
MONGO_AUTH = os.getenv('MONGO_AUTH')
client = MongoClient(f"mongodb+srv://{MONGO_AUTH}@{MONGO_URL}/?retryWrites=true&w=majority&appName=ubap")
client.admin.command('ping')
print("Pinged your deployment. You successfully connected to MongoDB!")

# Select the database and collection
db = client['ubap']
collection = db['data']

@app.route('/')
def hello():
    return 'Hello, Flask! This is the ubap-api.'

@app.route('/get/uxv', methods=['GET'])
def get_uxv():
    # Get the current time
    now = datetime.now()

    # Query to get all documents with type 'uxv'
    documents = collection.find({"type": "uxv"})

    # Dictionary to store the latest document for each uxv_id
    latest_uxv_documents = {}

    # Process each document
    for doc in documents:
        uxv_id = doc['uxv_id']
        timestamp = doc['timestamp']
        # timestamp = datetime.strptime(doc['timestamp'], "%Y-%m-%d %H:%M:%S.%f")

        # Update the latest document for each uxv_id
        if uxv_id not in latest_uxv_documents or timestamp > latest_uxv_documents[uxv_id]['timestamp']:
            latest_uxv_documents[uxv_id] = {
                'timestamp': timestamp,
                'location': doc['location'],
                'goal': doc['goal']
            }

    # Prepare the response
    response = {}
    for uxv_id, data in latest_uxv_documents.items():
        # Determine status
        if now - data['timestamp'] <= timedelta(minutes=5):
            status = 'online'
        else:
            status = 'offline'

        # Build the response
        response[uxv_id] = {
            'location': data['location'],
            'goal': data['goal'],
            'status': status
        }

    return jsonify(response)

def serialize_document(doc):
    # Convert ObjectId to string and remove specified fields
    del doc['_id']
    for field in ['source', 'uxv_id', 'timestamp']:
        if field in doc:
            del doc[field]
    return doc

@app.route('/get/data', methods=['GET'])
def get_data():
    # Query to get all documents with type different from 'uxv'
    documents = collection.find({"type": {"$ne": "uxv"}})

    modified_documents = []
    for doc in documents:
        # Serialize the document to be JSON serializable and strip specific fields
        modified_doc = serialize_document(doc)
        modified_documents.append(modified_doc)

    return jsonify(modified_documents)

if __name__ == '__main__':
    app.run(debug=True)
