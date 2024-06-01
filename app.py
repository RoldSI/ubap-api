from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
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
    return '/get/uxv endpoint'

@app.route('/get/data', methods=['GET'])
def get_data():
    return '/get/data endpoint'

if __name__ == '__main__':
    app.run(debug=True)
