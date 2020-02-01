from flask import render_template
from app import app

@app.route('/')
def index():
   return render_template('output_basic_form.html')