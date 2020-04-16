from dotenv import load_dotenv
import os

from flask import render_template, jsonify, request

from . import app
from . import utils

load_dotenv()

@app.route("/")
def home():
    SECRET_VAR = os.getenv("MAVARIABLE")
    print('MAVARIABLE : ', SECRET_VAR)
    return render_template("index.html")

@app.route("/ajax", methods=["POST"])
def ajax():
    user_text = request.form["user_text"]
    response = utils.transform(user_text)
    print('response : ', response)
    return jsonify(response)
