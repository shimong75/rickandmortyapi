import requests
import json
import csv
from flask import Flask, request
import os.path
from utils import log
from utils.characters_csv import create_csv
from utils.normalize_query import normalize

logger = log.init_logger('Flask_app', testing_mode=False)
app = Flask(__name__)


@app.route('/')
@app.route('/healthcheck')
def health_check():
    logger.info("health_check")
    res = requests.get('https://rickandmortyapi.com/api/character/')
    return res.reason, res.status_code


@app.route('/all')
def fetch_all():
    characters = []
    without_cache = request.args.get("without_cache", 'False')
    if not os.path.exists('the_right_characters.csv') and without_cache.lower not in ['true', '1', 't', 'y', 'yes']:
        create_csv()
    with open('the_right_characters.csv') as csv_file:
        reader = csv.reader(csv_file)
        for character in reader:
            # logger.info(character)
            characters.append({
                "Name": character[0],
                "Location": character[1],
                "Link": character[2]
            })
    return json.dumps(characters, indent=4, sort_keys=True), 200


@app.route('/characters')
def fetch_characters():
    without_cache = request.args.get("without_cache", 'False')
    if not os.path.exists('the_right_characters.csv') and without_cache.lower not in ['true', '1', 't', 'y', 'yes']:
        create_csv()
    if not request.args or "name" not in request.args:
        return "Pls add query_params in format name=<character name>", 422
    with open('the_right_characters.csv') as csv_file:
        query_params = normalize(request.args)
        reader = csv.reader(csv_file)
        characters = []
        for character in reader:
            if character[0] in query_params["name"]:
                characters.append({
                    "Name": character[0],
                    "Location": character[1],
                    "Link": character[2]
                })
        return json.dumps(characters, indent=4, sort_keys=True), 200


@app.route('/locations')
def fetch_locations():
    without_cache = request.args.get("without_cache", 'False')
    if not os.path.exists('the_right_characters.csv') and without_cache.lower not in ['true', '1', 't', 'y', 'yes']:
        create_csv()
    if not request.args or "location" not in request.args:
        return "Pls add query_params in format location=<location name>", 422
    with open('the_right_characters.csv') as csv_file:
        query_params = normalize(request.args)
        reader = csv.reader(csv_file)
        characters = []
        for character in reader:
            if character[1].lower() in query_params["location"].lower():
                characters.append({
                    "Name": character[0],
                    "Location": character[1],
                    "Link": character[2]
                })
        return json.dumps(characters, indent=4, sort_keys=True), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)




