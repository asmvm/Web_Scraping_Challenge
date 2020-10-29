from flask import Flask, render_template, redirect
from pymongo import MongoClient as MC
import scrape_mars

# Use PyMongo to establish Mongo connection
mongo = MC()
db = mongo.mars_app
col = db.mars_data

# Create an instance of Flask
app = Flask(__name__)


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = col.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():    

    # Run the scrape function
    # mars_data = mongo.db.mars_data
    data = scrape_mars.scrape_all()

    # Update the Mongo database using update and upsert=True
    col.insert(data)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
