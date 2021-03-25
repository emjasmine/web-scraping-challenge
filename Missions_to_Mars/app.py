from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars  

# Creates application
app = Flask(__name__)

# setup mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

