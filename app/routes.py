from flask import  Flask, redirect, url_for, render_template, request
from app import app


@app.route('/',methods=["GET", "POST"])
def index():
   if request.method == "POST":
      stat_type = request.form['statistics']
      if stat_type == "basic":
         return redirect(url_for('basic'))
      else:
         return redirect(url_for('descriptive'))
   else:
      return render_template('input_form.html')

@app.route('/basic', methods=["GET", "POST"])
def basic():
   return render_template('output_basic_form.html')

@app.route('/descriptive',methods=["GET", "POST"])
def descriptive():
   return render_template('output_descriptive_form.html')