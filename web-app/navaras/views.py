"""

Routes and Views

"""

from flask import render_template
from navaras import app

@app.route('/')
def home():
    return render_template('index.html')