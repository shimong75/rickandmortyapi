import requests
import json
import csv
from utils import log

logger = log.init_logger('APP', testing_mode=False)


def create_csv():
    the_characters = get_all_characters()
    with open('the_right_characters.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for character in the_characters:
            writer.writerow(character)
        logger.info("File created")


def get_all_characters():
    the_characters = []
    is_next = 'https://rickandmortyapi.com/api/character/?page1'
    while is_next:
        logger.info(f"characters in page {is_next}:")
        characters_in_page, is_next = get_page(is_next)
        for character in characters_in_page:
            logger.info(character)
            the_characters.append(character)
    return the_characters


def get_page(url: str) -> list:
    try:
        res = requests.get(url)
    except Exception as e:
        logger.info(f"Failed to Fetch data from {url}")
    parsed_results = json.loads(res.text)['results']
    is_next = json.loads(res.text)['info']['next']
    the_characters = []
    for item in parsed_results:
        if item['species'] == 'Human' and item['status'] == 'Alive' and 'Earth' in item['origin']['name']:
            the_characters.append([item['name'], item['location']['name'], item['image']])
    return [the_characters, is_next]