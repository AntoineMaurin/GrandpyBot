from flask import render_template, jsonify, request

from dotenv import load_dotenv

from app.API.Gmaps.gmaps_interaction import GmapsInteraction
from app.API.Wikimedia.geosearch_interaction import GeoSearchInteraction
from app.API.Wikimedia.wikimedia_interaction import WikimediaInteraction

from . import app
from . import utils

import json
import os

load_dotenv()

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
    # response_dict['API_KEY'] = os.environ['API_KEY']

    if 'error_msg' in response.keys():
        print(response_dict)
        response_dict['error_msg'] = response['error_msg']
        return jsonify(response_dict)
    else:
        # Wikimedia call
        geo_search_obj = GeoSearchInteraction((response['lat'],
                                               response['lng']))
        list_ids = geo_search_obj.get_page_id()

        wiki_obj = WikimediaInteraction(list_ids)
        wiki_response_dict = wiki_obj.get_content()

        masculin = ["tunnel", "boulevard", "musée", "buste", "conservatoire", "quartier", "lac", "puy", "logis", "palais", "théâtre", "lycée", "cimetière", "stade", "château", "prieuré"]
        feminin = ["rue", "chapelle", "maison", "préfecture", "cité", "grande", "place", "patinoire", "cour", "tour"]
        apostrophe = ["hôtel", "avenue", "allée", "exposition", "arrondissement", "église", "île", "échevinage", "espace", "abbaye"]
        pluriel = ["galeries"]

        if wiki_response_dict['title'].split()[0].lower() in masculin:
            article = "trouve le "
        elif wiki_response_dict['title'].split()[0].lower() in feminin:
            article = "trouve la "
        elif wiki_response_dict['title'].split()[0].lower() in pluriel:
            article = "trouvent les "
        elif wiki_response_dict['title'].split()[0].lower() in apostrophe:
            article = "trouve l'"
        else:
            article = "trouve"

        print('\nrésultat wikimédia : ', wiki_response_dict['text'], '\n')
        grandpy_msg = ("Cela se trouve au " + response['address'] +
                       ", d'ailleurs savais-tu que tout proche se " +
                       article + wiki_response_dict['title'] + " ? " +
                       wiki_response_dict['text'])

        response_dict['grandpy_msg'] = grandpy_msg
        response_dict['url'] = wiki_response_dict['url']
        response_dict['lat'] = response['lat']
        response_dict['lng'] = response['lng']

        print(response_dict)
        return jsonify(response_dict)
