from flask import render_template, jsonify, request

from app.API.Gmaps.gmaps_interaction import GmapsInteraction
from app.API.Wikimedia.geosearch_interaction import GeoSearchInteraction
from app.API.Wikimedia.wikimedia_interaction import WikimediaInteraction
from app.Grandpy.build_response import BuildResponse

from . import app

import json
import os

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/thinking", methods=["POST"])
def thinking():
    user_text = request.form["user_text"]

    obj = BuildResponse(user_text)
    response_dict = obj.get_response()

    return jsonify(response_dict)
