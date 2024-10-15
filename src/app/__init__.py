from flask import Flask

app = Flask(__name__, static_folder='static')
app.secret_key = 'testing_secret'

from app import routes