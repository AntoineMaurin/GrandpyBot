from flask import render_template, jsonify, request

from app.API.Gmaps.gmaps_interaction import GmapsInteraction
from app.API.Gmaps.address_parsing import AddressParsing

from app.API.Wikimedia.wikimedia_interaction import WikimediaInteraction

from . import app
from . import utils

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ajax", methods=["POST"])
def ajax():
    user_text = request.form["user_text"]
    # Askin G-Maps API to get the place
    gmap = GmapsInteraction(user_text)
    response = gmap.get_content()
    print('response : ', response)
    # Parsing the address to ask Wikimedia about the place
    wiki_search = AddressParsing.parse(response['address'])
    # Wikimedia call
    wiki_obj = WikimediaInteraction(wiki_search)
    wiki_response = wiki_obj.get_content()
    return jsonify(wiki_response)
