from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars



app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)
#mongo = PyMongo(app, url="mongodb://localhost:27017/mars")


@app.route('/')
def index():
    listings = mongo.db.listings.find_one()
    return render_template('index.html', listings=listings)


@app.route('/scrape')
def get():
    listings = mongo.db.listings
    listings_data = scrape_mars.scrape()
    listings.update({}, listings_data, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)