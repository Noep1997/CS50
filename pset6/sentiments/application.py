from flask import Flask, redirect, render_template, request, url_for

import helpers
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    # validate screen_name
    screen_name = request.args.get("screen_name")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name, 100)

    # call Analyzer function
    analyzer = Analyzer()

    # initialize positive, negative, neutral and total count to zero
    positive_count, negative_count, neutral_count, total = 0, 0, 0, 0

    # analyze tweets, storing the number of each type of tweets in a count
    for tweet in tweets:
        score = analyzer.analyze(tweet)
        total += 1
        if score > 0.0:
            positive_count += 1
        elif score < 0.0:
            negative_count += 1
        else:
            neutral_count += 1

    # convert the count of each type of tweet in percentage
    positive, negative, neutral = positive_count / total * 100.0, negative_count / total * 100.0, neutral_count / total * 100.0

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
