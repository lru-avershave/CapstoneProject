from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from flask_caching import Cache
import os
from mongoengine import *

connect('testDB', 
        host='localhost', 
        port=27017)
cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['CACHE_TYPE'] = 'simple'
bootstrap = Bootstrap(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/testDB"
mongo = PyMongo(app)
cache = Cache()
cache.init_app(app)

from app import routes