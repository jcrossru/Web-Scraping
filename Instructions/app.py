from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
#mongo = PyMongo(app)

# Or set inline
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")


@app.route("/")
def index():
    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scraper():
    #listings = mongo.db.listings
    mars_data = scrape_mars.scrape_info()
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
