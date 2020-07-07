from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os


app = Flask(__name__)

mongo = PyMongo(
    app, uri = os.environ.get("MONGODB_URI"))


@app.route("/")
def home():

    mars_data = mongo.db.listings.find_one()

    return render_template("index.html", mars=mars_data)


@app.route("/scrape")
def scrape():

    listings = mongo.db.listings
    listings_data = scrape_mars.scrape_data()
    listings.update({}, listings_data, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
