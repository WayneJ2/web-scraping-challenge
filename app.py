from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    marsData = mongo.db.marsPull.find_one()
    return render_template("index.html", mars=marsData)

@app.route("/scrape")
def scraper():
    marsData = mongo.db.marsPull
    mars_data = scrape_mars.scrape()
    print(mars_data)
    marsData.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)