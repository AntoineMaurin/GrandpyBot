from flask import render_template, jsonify, request

from . import app
from . import utils

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ajax", methods=["POST"])
def ajax():
    user_text = request.form["user_text"]
    response = utils.transform(user_text)
    print('response : ', response)
    return jsonify(response)
