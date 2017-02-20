'''from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome Home'


#------------- App Launch---------
if __name__ == '__main__':
    app.secret_key = 'superman__12'
    app.debug = True
    app.run(host='0.0.0.0', port=5001)'''