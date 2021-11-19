import json
from pymongo import MongoClient
from flask import Flask, jsonify
from flask_mongoengine import MongoEngine



app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'ProjectX',
    'host': 'mongodb+srv://Tashkov:<password>@cluster0.ic3c3.mongodb.net/ProjectX?retryWrites=true&w=majority',
    'port': 27017,
}
db = MongoEngine()
db.init_app(app)


# client = MongoClient("mongodb+srv://Tashkov:JNhCHW8nFPkluxLN@cluster0.ic3c3.mongodb.net/ProjectX?retryWrites=true&w=majority")
# db = client["ProjectX"]
# collection = db["tweets"]

@app.route('/')
def index():
    return('Home page')

# @app.route('/test')
# def add_data():
#     some_data = {
#         '_id': 2,
#         'name': 'Ico',
#         'age': 28    
#     }
#     try:
#         collection.insert_one(some_data)
#         return ("OK")
#     except:
#         return ("ERROR!")

# @app.route('/populate', methods=['POST'])
# def populate_db():
    
#     dat = list()
#     with open('elonmusk.json') as elon:
#         for line in elon.readlines():
#             if not line.strip():
#                 continue

#             json_data = json.loads(line)
#             dat.append(json_data)

#     for tweet in dat:
#         tweet.save()
#         return jsonify(tweet), 201

if __name__=='__main__':
    app.run(debug=True)