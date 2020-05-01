from flask import render_template, jsonify, request

from app.API.Gmaps.gmaps_interaction import GmapsInteraction
from app.API.Wikimedia.geosearch_interaction import GeoSearchInteraction
from app.API.Wikimedia.wikimedia_interaction import WikimediaInteraction
from app.Grandpy.grandpy_thinks import GrandpyThinks

from . import app

import json
import os

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/thinking", methods=["POST"])
def thinking():
    user_text = request.form["user_text"]

    obj = GrandpyThinks(user_text)
    response_dict = obj.reflection()
    print("\n\n\n", response_dict, "\n\n\n")
    return jsonify(response_dict)
