'''
author: ankush.shah.nitk@gmail.com
date: 29th Nov 2015
desc: calculate the environment score using
      Behavior Risk Model Algorithm (brma)
'''

import json
import logging
import requests
import urllib


def get_aqi_score(loc_data):
    api_url = 'http://api.breezometer.com/baqi/?'
    api_key = '906d4d728056496b85b059e335a17a18'
    params = {}
    params['key'] = api_key
    total_aqis = 0.0
    total_time_spent = 0.0
    for key in loc_data:
        (lati, longi) = key
        time_spent = loc_data[key]
        params['lat'] = lati
        params['lon'] = longi
        data = urllib.urlencode(params)
        res = requests.get(api_url + data)
        res = json.loads(res.text)
        if 'breezometer_aqi' in res:
            total_aqis += res['breezometer_aqi'] * time_spent
            total_time_spent += time_spent

    if total_time_spent > 0:
        avg_aqi = total_aqis / total_time_spent
        aqi_score = (100 - avg_aqi) * 12.5 / 100
        aqi_score = min(max(0, aqi_score), 12.5)
        return aqi_score
    else:
        return None


def get_env_score(loc_data):
    env_score = {}
    nimby_score = get_aqi_score(loc_data)
    env_score['aqi'] = nimby_score

    return env_score


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    loc_data = {
                (50.73858, 7.07873): 120,  # McFit in bonn
                (50.737204, 7.102983): 120,  # Subway
                (37.757815, -122.5076408): 120,  # San Francisco
                (40.7058316, -74.2582003): 120  # New York
            }

    env_score = get_env_score(loc_data)
    print env_score
