from flask import Flask, make_response
from flask import render_template
app = Flask(__name__)

from src import routes

@app.route('/favicon.ico')
def favicon():
    return make_response("", 204)

if __name__ == '__main__':
    app.run(debug=True)