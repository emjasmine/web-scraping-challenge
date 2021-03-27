from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars  

# Creates application
app = Flask(__name__)

# setup mongo connection
#conn = 'mongodb://localhost:27017'
#client = pymongo.MongoClient(conn)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_db'
mongo = PyMongo(app)
################################################################################
#Home Route
################################################################################

@app.route("/")
def Home ():
    #there should be a button on the main homepage that will use the scrape route
    #pull the data that was scraped by the scrape function to display on the main page
    info = mongo.db.mars.find_one()
    return render_template('index.html', info = info )

##################################################################################
#Scrape Route
##################################################################################

@app.route("/scrape")
def scrape():
    #this route will use the scrape function from scrape_mars and push to mongodb
    #connect to the collections
    mars = mongo.db.mars
    scraped_info = scrape_mars.scrape()
    mars.update({}, scraped_info, upsert = True)
    return redirect('/', code = 302)

#######################################

if __name__ == '__main__':
    app.run(debug=True)