from flask import Flask

app = Flask(__name__)
app.secret_key = 'testing_secret'

from app import routes