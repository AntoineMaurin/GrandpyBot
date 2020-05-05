from flask import render_template, jsonify, request

from app.Grandpy.grandpy import Grandpy

from . import app


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/answer", methods=["POST"])
def answer():
    user_text = request.form["user_text"]

    obj = Grandpy(user_text)
    response_dict = obj.get_response()

    return jsonify(response_dict)
