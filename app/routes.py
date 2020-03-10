from flask import  Flask, redirect, url_for, render_template, request, jsonify, send_file
from flask_excel import make_response
from app import app, cache
from models.SavedPage import SavedPage
from TweetsToDB.TweetModel import Tweet
from mongoengine import *
import pandas as pd
import orjson
from utils.Tweet import GetTweet
from utils.Stats import statTweets
from utils.TweetCounter import locationCounter
from utils.FileSaver import exportToFile, to_tde

from serverside.TableModel import TableBuilder
from serverside.serverside_table import ServerSideTable
from models.PageClass import Page

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
   locationTotals = locationCounter(reqTweet)
   return render_template('output_basic_form.html', _id=_id, filters=reqPage[0], locTotals = locationTotals, tweets=reqTweet)

@app.route('/descriptive/<_id>',methods=["GET", "POST"])
def descriptive(_id):
   reqPage = GetTweet(_id)
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

@app.route('/serverside/<_id>', methods=['GET'])
def serverside(_id):
   reqTweet, reqPage = GetTweet(_id)
   table = TableBuilder()
   data = table.collect_data_serverside(request, orjson.loads(reqTweet.to_json())) ### THIS IS SLOW WITH A BIG QUERY
   return jsonify(data)

@app.route('/downloadfiles', methods=['GET', 'POST'])
def generateFile():
   fileName = request.form.get('file_name')
   #file = exportToFile(fileName)
   sample = to_tde(fileName)
   return send_file("test.tde", as_attachment=True)
