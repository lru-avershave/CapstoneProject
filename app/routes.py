from flask import  Flask, redirect, url_for, render_template, request, jsonify, send_file, flash,session
from app import app, cache
from mongoengine import *
from TweetsToDB.TweetModel import Tweet
from utils.Tweet import GetTweet
from utils.Stats import statTweets
from utils.TweetCounter import locationCounter
from utils.FileSaver import exportToFile
from utils.Login import validate
from serverside.TableModel import TableBuilder
from serverside.serverside_table import ServerSideTable
from models.PageClass import Page
from models.SavedPage import SavedPage
import pandas as pd
import orjson

#Home page route for start up
@app.route('/',methods=["GET", "POST"])
def index():
   return render_template('input_form.html')

#Retrieves user inputted values before loading stat page
#Collects filters and redirects based on stat type
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

#Route to load the basic stats page
#Generates location totals as well
#Shortcircuits results if query is zero
@app.route('/basic/<_id>', methods=["GET", "POST"])
def basic(_id):
   reqTweet, reqPage = GetTweet(_id)
   locationTotals = locationCounter(reqTweet)

   if reqTweet.count() == 0:
      flash('No results found!')
      return redirect((url_for("index")))
   
   return render_template('output_basic_form.html', _id=_id, filters=reqPage[0], locTotals = locationTotals, tweets=reqTweet)

#Route to load the descriptive page
#Shortcircuits results if query is zero
@app.route('/descriptive/<_id>',methods=["GET", "POST"])
def descriptive(_id):
   reqTweet, reqPage = GetTweet(_id)

   if reqTweet.count() == 0:
      flash('No results found!')
      return redirect((url_for("index")))

   return render_template('output_descriptive_form.html', _id=_id)

@app.route('/id', methods=['POST'])
def id():
   _id = request.form.get('old_output')
   reqPage = SavedPage.objects(id=_id)

   if reqPage[0]['pageType'] == "basic":
      return redirect(url_for('basic', _id=_id))
   
   if reqPage[0]['pageType'] == "descriptive":
      return redirect((url_for('descriptive', _id=_id)))


@app.route('/serverside/<_id>', methods=['GET'])
def serverside(_id):
   reqTweet, reqPage = GetTweet(_id)
   table = TableBuilder()
   data = table.collect_data_serverside(request, orjson.loads(reqTweet.to_json())) ### THIS IS SLOW WITH A BIG QUERY
  
   return jsonify(data)

#Renders template based on validation results
#Goes to admin form on success, login form on failure
@app.route('/admin/', methods=['GET', 'POST'])
def admin():
   if not session.get('logged_in'):
      return render_template('admin_login_form.html')
   else:
      return render_template('admin_form.html')

#Retrieves inputted username and password
#Validates them against saved credentials
##Sets login status based on results, redirects to admin route
@app.route('/admin/login', methods=['GET', 'POST'])
def adminlogin():
   username = request.form.get('loginFormUsername')
   password = request.form.get('loginFormPassword')
  
   if not validate(username, password):
      flash("Invalid Credentials")
      return redirect((url_for('admin')))
  
   session['logged_in'] = True
   return redirect((url_for('admin')))

#Route for downloading the excel file
#Retrieves the filename and downloads the temporary file to the client
@app.route('/downloadfiles', methods=['GET', 'POST'])
def generateFile():
   fileName = request.form.get('file_name')
   str_io = exportToFile()
  
   return send_file(str_io,
                 attachment_filename=fileName + '.xlsx',
                 as_attachment=True)
   
#Route used to logout on the admin page
#Changes login to false and redirects to home page
@app.route('/admin/logout', methods=['GET', 'POST'])
def logout():
   session['logged_in'] = False
  
   return redirect(url_for('index'))