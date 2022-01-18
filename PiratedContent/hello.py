from flask import Flask

import extractInfo

app = Flask(__name__)

@app.route("/")
def hello_world():
    return extractInfo.getData()