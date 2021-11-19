import json
import re
from pymongo import MongoClient, InsertOne
from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from bson.json_util import dumps, loads



app = Flask(__name__)

# app.config['MONGODB_SETTINGS'] = {
#     'db': 'ProjectX',
#     'host': 'mongodb+srv://Tashkov:<password>@cluster0.ic3c3.mongodb.net/ProjectX?retryWrites=true&w=majority',
#     'port': 27017,
# }
# db = MongoEngine()
# db.init_app(app)


client = MongoClient("mongodb+srv://Tashkov:<password>@cluster0.ic3c3.mongodb.net/ProjectX?retryWrites=true&w=majority")
db = client["ProjectX"]
collection = db["tweets"]

# Initialy populating the DB don't change the value 
# until a better condition is found
populated = True

if not populated:
    requesting = list()
    with open(r'elonmusk.json') as f:
        for jsonObj in f.readlines():
            if not jsonObj.strip():
                continue

            myDict = json.loads(jsonObj)
            requesting.append(InsertOne(myDict))

    result = collection.bulk_write(requesting)
    client.close()


cursor = db.collection.find_one({"date": "2020-06-28"})
print(cursor)

print("ok")

@app.route('/')
def index():
    return('Home page')

# doesn't work
@app.route('/date')
def tweets_by_date():
    cursor = db.collection.find()
    resp = dumps(cursor)
  
    return resp

    
if __name__=='__main__':
    app.run(debug=True)
