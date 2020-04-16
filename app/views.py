from dotenv import load_dotenv
import os

from flask import render_template, jsonify, request

from . import app
from . import utils

load_dotenv()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ajax", methods=["POST"])
def ajax():
    SECRET_VAR = os.environ['MAVARIABLE']
    user_text = request.form["user_text"]
    response = utils.transform(user_text)
    print('response : ', response)
    print('MAVARIABLE : ', SECRET_VAR)
    return jsonify(SECRET_VAR)
