'''
* Copyright ProjectVisionHealth (c) 2015
* Author Name: Ankush Shah
* Date : 22 Dec 2015
* Description: Module for calculating the nimby, yimby and
               the final brma score
'''

import json
import logging
import env_scorer
import requests
import yaml

from pprint import pprint

LOGGER = logging.getLogger(__name__)

CONFIG = yaml.load(open("config.yaml"))

PLACE_API = CONFIG['APIS']['google_place_api']
API_KEY = CONFIG['APIS']['google_place_api_key']

YIMBY_LOCS = CONFIG["YIMBY"]
NIMBY_LOCS = CONFIG["NIMBY"]
RADIUS = 20  # in meters


def get_nimby_score(loc_data):
    params = {'key': API_KEY,
              'radius': RADIUS,
              'types': '|'.join(NIMBY_LOCS)}
    score = 0
    for (lati, longi) in loc_data:
        params['location'] = '%s,%s' % (lati, longi)
        res = requests.get(PLACE_API, params=params)
        res = json.loads(res.text)
        if len(res['results']) > 0:
            score += 5

    score = min(score, 50)
    return score


def get_yimby_score(loc_data):
    params = {'key': API_KEY,
              'radius': RADIUS,
              'types': '|'.join(YIMBY_LOCS)}
    score = 50
    for (lati, longi) in loc_data:
        params['location'] = '%s,%s' % (lati, longi)
        res = requests.get(PLACE_API, params=params)
        res = json.loads(res.text)
        if len(res['results']) > 0:
            score -= 5

    score = max(score, 0)
    return score


def get_brma_score(loc_data):
    score = {}
    nimby_score = get_nimby_score(loc_data)
    score['nimby_score'] = nimby_score

    yimby_score = get_yimby_score(loc_data)
    score['yimby_score'] = yimby_score

    env_score = env_scorer.get_env_score(loc_data)
    score['environment_score'] = env_score

    score['brma_score'] = env_score['normalized_environment_score'] + nimby_score + yimby_score

    return score

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    loc_data = {
                (50.73858, 7.07873): 120,  # McFit in bonn
                (50.737204, 7.102983): 120,  # Subway
                (37.757815, -122.5076408): 120,  # San Francisco
                (40.7058316, -74.2582003): 120  # New York
            }

    score = get_brma_score(loc_data)
    print score
