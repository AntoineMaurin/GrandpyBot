from flask import render_template, jsonify, request

from app.API.Gmaps.gmaps_interaction import GmapsInteraction
from app.API.Gmaps.address_parsing import AddressParsing

from app.API.Wikimedia.wikimedia_interaction import WikimediaInteraction

from . import app
from . import utils

import json

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ajax", methods=["POST"])
def ajax():
    user_text = request.form["user_text"]
    # Askin G-Maps API to get the place
    gmap = GmapsInteraction(user_text)
    response = gmap.get_content()
    print('\nréponse google maps : ', response, '\n')
    response_dict = {}
    response_dict['user_text'] = user_text

    if 'error_msg' in response.keys():
        print(response_dict)
        response_dict['error_msg'] = response['error_msg']
        return jsonify(response_dict)
    else:
        # Parsing the address to ask Wikimedia about the place
        wiki_search = AddressParsing.parse(response['address'])
        print('\nrecherche wikimédia : ', wiki_search, '\n')
        # Wikimedia call
        # print(wiki_search)
        wiki_obj = WikimediaInteraction(wiki_search)
        wiki_response = wiki_obj.get_content()
        print('\nrésultat wikimédia : ', wiki_response, '\n')

        response_dict['wiki_response'] = wiki_response
        response_dict['lat'] = response['lat']
        response_dict['lng'] = response['lng']

        print(response_dict)
        return jsonify(response_dict)
