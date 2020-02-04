from flask import  Flask, redirect, url_for, render_template, request, flash
from app import app
from models.SavedPage import SavedPage
from mongoengine import *


@app.route('/',methods=["GET", "POST"])
def index():
   return render_template('input_form.html')

@app.route('/stats', methods=['POST'])
def stats():
   stat_type = request.form.get('statistics')
   filter_term = request.form.get('input_term')
   newPage = SavedPage(pageType=stat_type, filterTerm=filter_term).save()
   if stat_type == "basic":
      return redirect((url_for('basic', _id=newPage.id)))
   else:
      return redirect((url_for('descriptive', _id=newPage.id)))

@app.route('/basic/<_id>', methods=["GET", "POST"])
def basic(_id):
   reqPage = SavedPage.objects(id=_id)
   return render_template('output_basic_form.html', _id=_id)

@app.route('/descriptive/<_id>',methods=["GET", "POST"])
def descriptive(_id):
   reqPage = SavedPage.objects(id=_id)
   return render_template('output_descriptive_form.html', _id=_id)

@app.route('/id', methods=['POST'])
def id():
   _id = request.form.get('old_output')
   reqPage = SavedPage.objects(id=_id)
   if reqPage[0]['pageType'] == "basic":
      return redirect(url_for('basic', _id=_id))
   if reqPage[0]['pageType'] == "descriptive":
      return redirect((url_for('descriptive', _id=_id)))