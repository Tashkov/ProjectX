import json
from flask.wrappers import Response
from pymongo import MongoClient, InsertOne
from flask import Flask, render_template
from bson import  json_util


app = Flask(__name__)

client = MongoClient("mongodb+srv://Tashkov:<password>@cluster0.ic3c3.mongodb.net/ProjectX?retryWrites=true&w=majority")
db = client["ProjectX"]
collection = db["tweets"]

# Initialy populating the DB don't change the value 
# until a better condition is found
# Change the value to False if DB is empty
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



@app.route('/')
def index():
    return render_template('index.html')

# Displays the tweets created at the wanted date with the format YYYY-MM-DD
@app.route('/date/<string:date>', methods=["GET"])
def tweets_by_date(date):
    try:
        data = list(collection.find({"date": date}))
        for tweet in data:
            tweet["_id"] = str(tweet["_id"])
        return Response(
            response= json.dumps(data),
            status=500,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(response= json.dumps({"message": "cannot read tweets"}), status=500,mimetype="application/json")

if __name__=='__main__':
    app.run(debug=True)
