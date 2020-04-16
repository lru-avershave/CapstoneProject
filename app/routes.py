from flask import  Flask, redirect, url_for, render_template, request, jsonify, send_file, flash,session
from app import app, cache
from TweetsToDB.TweetModel import Tweet
from utils.Tweet import GetTweet
from utils.Stats import statTweets
from utils.TweetCounter import locationCounter
from utils.Login import validate
from serverside.TableModel import TableBuilder
from serverside.serverside_table import ServerSideTable
from models.SavedPage import SavedPage
import pandas as pd
import ujson


#Home page route for start up
@app.route('/',methods=["GET", "POST"])
def index():
   return render_template('input_form.html')

#Retrieves user inputted values before loading stat page
#Collects filters and redirects based on stat type
@app.route('/stats', methods=['POST'])
def stats():
   stat_type = request.form.get('statistics')
   if stat_type == None:
      stat_type = "Admin"
   filter_term = request.form.get('input_term')
   filter_time = request.form.get('input_time')
   filter_date = request.form.get('input_date')
   filter_location = request.form.get('input_location')
   filter_profile = request.form.get('input_profile')
  
   newPage = SavedPage(pageType=stat_type, filterTerm=filter_term, filterTime=filter_time, location=filter_location, tweetCreator=filter_profile, filterDate=filter_date).save()
  
   if stat_type == "basic":
      return redirect((url_for('basic', _id=newPage.id)))
   elif stat_type == "descriptive":
      return redirect((url_for('descriptive', _id=newPage.id)))
   else:
      return redirect((url_for('admin_delete_page', _id=newPage.id)))

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

   #This is hard coded and needs to be changed
   if reqTweet.count() > 290000:
      flash('WARNING: This queried the entire database! Please limit your options...')
      return redirect((url_for("index")))
   
   return render_template('output_basic_form.html', _id=_id, filters=reqPage[0], locTotals = locationTotals, tweets=reqTweet)

#Route to load the descriptive page
#Shortcircuits results if query is zero
@app.route('/descriptive/<_id>',methods=["GET", "POST"])
def descriptive(_id):
   reqTweet, reqPage = GetTweet(_id)

   stats = statTweets(toTweetJson(reqTweet, _id))

   if reqTweet.count() == 0:
      flash('No results found!')
      return redirect((url_for("index")))
   
   #This is hard coded and needs to be changed
   if reqTweet.count() > 290000:
      flash('WARNING: This queired the entire database! Please limit your options...')
      return redirect((url_for("index")))

   return render_template('output_descriptive_form.html', _id=_id, filters=reqPage[0], stats=stats)

@app.route('/admin/<_id>',methods=["GET", "POST"])
def admin_delete_page(_id):
   reqTweet, reqPage = GetTweet(_id)

   stats = statTweets(toTweetJson(reqTweet, _id))

   if reqTweet.count() == 0:
      flash('No results found!')
      return redirect((url_for("index")))
   
   #This is hard coded and needs to be changed
   if reqTweet.count() > 290000:
      flash('WARNING: This queired the entire database! Please limit your options...')
      return redirect((url_for("index")))

   return render_template('output_admin_form.html', _id=_id, filters=reqPage[0])

'''
API that uses the ID in the url and redirects the user to the correct saved page.
'''
@app.route('/id', methods=['POST'])
def id():
   _id = request.form.get('old_output')
   reqPage = SavedPage.objects(id=_id)

   if reqPage[0]['pageType'] == "basic":
      return redirect(url_for('basic', _id=_id))
   
   if reqPage[0]['pageType'] == "descriptive":
      return redirect((url_for('descriptive', _id=_id)))
   
   if reqPage[0]['pageType'] == "Admin":
      return redirect((url_for('admin', _id=_id)))

'''
The index page uses a DataTable that does an ajax call in order to put data into the table.
This is needed to paginate the data. This also helps with sorting/searching the data on the data table.
'''
@app.route('/serverside/<_id>', methods=['GET'])
def serverside(_id):
   reqTweet, reqPage = GetTweet(_id)
   jsonTweet = toTweetJson(reqTweet, _id)
   table = TableBuilder()
   data = table.collect_data_serverside(request, jsonTweet)
   return jsonify(data)

@app.route('/adminserverside/<_id>', methods=['GET'])
def adminserverside(_id):
   reqTweet, reqPage = GetTweet(_id)
   jsonTweet = ujson.loads(reqTweet.to_json())
   table = TableBuilder()
   data = table.collect_data_serverside(request, jsonTweet)
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

#Route used to logout on the admin page
#Changes login to false and redirects to home page
@app.route('/admin/logout', methods=['GET', 'POST'])
def logout():
   session['logged_in'] = False
  
   return redirect(url_for('index'))

@app.route('/deleteTweet', methods=['GET'])
def deleteTweet():

    #Access arguments via request.args
    _tweetID = request.args.get('tweetID')
    deleteTweet = Tweet.objects(tweetID = _tweetID).first().delete()
    return 'TEST'
    

'''
This method is used strictly to cache the json data.
The DataTable does an ajax call every time you click to see the next page on the table.
This helps performance for the server side processing.
'''
@cache.memoize(5)
def toTweetJson(reqTweet, _id):
   jsonTweet = ujson.loads(reqTweet.to_json())
   return jsonTweet

