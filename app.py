from pymongo import MongoClient
from flask import Flask

app = Flask(__name__)

client = MongoClient("mongodb+srv://Tashkov:<password>@cluster0.ic3c3.mongodb.net/ProjectX?retryWrites=true&w=majority")
db = client["ProjectX"]
collection = db["tweets"]

@app.route('/')
def index():
    return('Home page')

@app.route('/test')
def add_data():
    some_data = {
        '_id': 2,
        'name': 'Ico',
        'age': 28    
    }
    try:
        collection.insert_one(some_data)
        return ("OK")
    except:
        return ("ERROR!")

if __name__=='__main__':
    app.run(debug=True)