from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import os
from mongoengine import *

connect('testDB', 
        host='localhost', 
        port=27017)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
bootstrap = Bootstrap(app)

from app import routes