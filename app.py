import json
import re
from pymongo import MongoClient, InsertOne
from flask import Flask, render_template, Response, request, jsonify



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

#Helper function to split the old date and return the new one
def date_builder(old_date: str, new_day):
    year, month, day = old_date.split('-')
    
    # accounting for the integers with leading 0
    if int(new_day) < 10:
        leading_zero = {
            1: "01",
            2: "02",
            3: "03",
            4: "04",
            5: "05",
            6: "06",
            7: "07",
            8: "08",
            9: "09"
        }
        new_day = leading_zero[int(new_day)]
    to_join = [year, month, new_day]
    return("-".join(to_join))


# Helper function to determine the range of the day:
def determine_date_range(from_date:str, to_date: str):
    from_lst= from_date.split("-")
    to_lst = to_date.split("-")
    fromY, fromM, fromD = int(from_lst[0]), int(from_lst[1]), int(from_lst[2])
    toY, toM, toD = int(to_lst[0]), int(to_lst[1]), int(to_lst[2])

    # if we`re looking in the same month
    if fromM == toM and fromD != toD:
        return int(fromD), int(toD)

@app.route('/')
def index():
    return render_template('index.html')

# Displays the tweets created at the wanted date with the format YYYY-MM-DD
@app.route('/date', methods=["GET"])
def tweets_by_date():

    date_from = request.args.get('from')
    
    try:
        data = list(collection.find({"date": date_from}))
        for tweet in data:
            tweet["_id"] = str(tweet["_id"])
        return Response(
            response= json.dumps(data),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(response= json.dumps({"message": "cannot read tweets"}), status=500,mimetype="application/json")


#Returns total tweets per day in a given range
@app.route('/tweets', methods=["GET"])
def tweets_for_day():
        
    # Using the template in the above endpoint, make a request to the DB
    # with the above variables as params
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    
    try:
        start, finish = determine_date_range(date_from, date_to)
        to_disp_lst = list()

        for day in range(start, finish + 1):
            day = str(day)
            date = date_builder(date_from, day)

            working_dict = dict()
            data = list(collection.find({"date": date}))
            total_daily_tweets = len(data)

        
            working_dict["date"] = date
            working_dict["total tweets"] = total_daily_tweets
            to_disp_lst.append(working_dict)

        return Response(
            response= json.dumps(to_disp_lst),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(response= json.dumps({"message": "cannot read tweets"}), status=500,mimetype="application/json")

# Returns the total likes for each day in a time frame
@app.route('/likes', methods=["GET"])
def likes_for_day():
        
    # Using the template in the above endpoint, make a request to the DB
    # with the above variables as params
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    
    try:
        start, finish = determine_date_range(date_from, date_to)
        to_disp_lst = list()

        for day in range(start, finish + 1):
            day = str(day)
            date = date_builder(date_from, day)

            working_dict = dict()
            data = list(collection.find({"date": date}))
            total_daily_likes = 0

            for tweet in data:
                tweet["_id"] = str(tweet["_id"])
                tweet_likes = int(tweet["likes_count"])
                total_daily_likes += tweet_likes
        
            working_dict["date"] = date
            working_dict["total likes"] = total_daily_likes
            to_disp_lst.append(working_dict)

        return Response(
            response= json.dumps(to_disp_lst),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(response= json.dumps({"message": "cannot read tweets"}), status=500,mimetype="application/json")
        

# Returns the total likes for each day in a time frame
@app.route('/retweets', methods=["GET"])
def retweets_for_day():
        
    # Using the template in the above endpoint, make a request to the DB
    # with the above variables as params
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    
    try:
        start, finish = determine_date_range(date_from, date_to)
        to_disp_lst = list()

        for day in range(start, finish + 1):
            day = str(day)
            date = date_builder(date_from, day)

            working_dict = dict()
            data = list(collection.find({"date": date}))
            total_daily_retweets = 0

            for tweet in data:
                tweet["_id"] = str(tweet["_id"])
                retweets = int(tweet["retweets_count"])
                total_daily_retweets += retweets
        
            working_dict["date"] = date
            working_dict["total retweets"] = total_daily_retweets
            to_disp_lst.append(working_dict)

        return Response(
            response= json.dumps(to_disp_lst),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(response= json.dumps({"message": "cannot read tweets"}), status=500,mimetype="application/json")


#Returns the total count of replies
@app.route('/replies', methods=["GET"])
def replies_for_day():
        
    # Using the template in the above endpoint, make a request to the DB
    # with the above variables as params
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    
    try:
        start, finish = determine_date_range(date_from, date_to)
        to_disp_lst = list()

        for day in range(start, finish + 1):
            day = str(day)
            date = date_builder(date_from, day)

            working_dict = dict()
            data = list(collection.find({"date": date}))
            total_daily_replies = 0

            for tweet in data:
                tweet["_id"] = str(tweet["_id"])
                tweet_replies = int(tweet["replies_count"])
                total_daily_replies += tweet_replies
        
            working_dict["date"] = date
            working_dict["total replies"] = total_daily_replies
            to_disp_lst.append(working_dict)

        return Response(
            response= json.dumps(to_disp_lst),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(response= json.dumps({"message": "cannot read tweets"}), status=500,mimetype="application/json")

if __name__=='__main__':
    app.run(debug=True)
