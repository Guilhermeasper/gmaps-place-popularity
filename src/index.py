from flask import Flask, Response, jsonify
from dotenv import load_dotenv
from popularity.popularity import Popularity

load_dotenv()


app = Flask(__name__)


@app.route("/<int:day>/<int:time>")
def get_time_popularity(day, time):
    if (day < 1 or day > 5):
        return jsonify(message="Invalid day"), 400
    elif (time < 6 or time > 23):
        return jsonify(message="Invalid time"), 400
    else:
        popularity = Popularity(day, time)
        return jsonify(percentage=popularity.get_popularity()), 200
