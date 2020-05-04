from flask import render_template, jsonify, request

from app.Grandpy.build_response import BuildResponse

from . import app


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/thinking", methods=["POST"])
def thinking():
    user_text = request.form["user_text"]

    obj = BuildResponse(user_text)
    response_dict = obj.get_response()

    return jsonify(response_dict)
