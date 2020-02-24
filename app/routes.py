from flask import  Flask, redirect, url_for, render_template, request, jsonify
from app import app
from models.SavedPage import SavedPage
from TweetsToDB.TweetModel import Tweet
from mongoengine import *
import pandas as pd
import json
from utils.Tweet import GetTweet
from utils.Stats import statTweets
from utils.LocationCounter import locationCounter

@app.route('/',methods=["GET", "POST"])
def index():
   return render_template('input_form.html')

@app.route('/stats', methods=['POST'])
def stats():
   stat_type = request.form.get('statistics')
   filter_term = request.form.get('input_term')
   filter_time = request.form.get('input_time')
   filter_location = request.form.get('input_location')
   filter_profile = request.form.get('input_profile')
   newPage = SavedPage(pageType=stat_type, filterTerm=filter_term, filterTime=filter_time, location=filter_location, tweetCreator=filter_profile).save()
   if stat_type == "basic":
      return redirect((url_for('basic', _id=newPage.id)))
   else:
      return redirect((url_for('descriptive', _id=newPage.id)))

@app.route('/basic/<_id>', methods=["GET", "POST"])
def basic(_id):
   reqTweet, reqPage = GetTweet(_id)
   locationCounter(reqTweet)
   return render_template('output_basic_form.html', _id=_id, tweets=reqTweet, filters=reqPage[0], locals = locations)

@app.route('/descriptive/<_id>',methods=["GET", "POST"])
def descriptive(_id):
   reqTweet, reqPage = GetTweet(_id) #Query for Tweet
   return render_template('output_descriptive_form.html', _id=_id)

@app.route('/id', methods=['POST'])
def id():
   _id = request.form.get('old_output')
   reqPage = SavedPage.objects(id=_id)
   if reqPage[0]['pageType'] == "basic":
      return redirect(url_for('basic', _id=_id))
   if reqPage[0]['pageType'] == "descriptive":
      return redirect((url_for('descriptive', _id=_id)))

@app.route('/admin/login', methods=['GET', 'POST'])
def adminlogin():
   return render_template('admin_login_form.html')

@app.route('/admin/landing', methods=['GET', 'POST'])
def adminlanding():
   return render_template('admin_form.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
   reqTweet = Tweet.objects()
   stats = statTweets(reqTweet)
   return str(stats)
   