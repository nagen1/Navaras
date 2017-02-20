"""

The navaras web application package

"""

from flask import Flask

app = Flask(__name__)
app.debug = True

import navaras.views