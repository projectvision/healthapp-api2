'''
* Copyright ProjectVisionHealth (c) 2015
* Author Name: Ankush Shah
* Date : 22 Dec 2015
* Description: Module for calculating environment metrics
'''

import json
import logging
import requests
import urllib
import crime_rate_api


def get_crime_score(loc_data):
    total_crime_score = 0.0
    total_time_spent = 0.0
    for key in loc_data:
        (lati, longi) = key
        time_spent = loc_data[key]
        crime_rate = crime_rate_api.get_crime_rate(lati, longi)
        if crime_rate is not None:
            total_crime_score += crime_rate * time_spent
            total_time_spent += time_spent

    if total_time_spent > 0:
        avg_crime_score = total_crime_score / total_time_spent
        crime_score = (avg_crime_score) * 12.5 / 100
        crime_score = min(max(0, crime_score), 12.5)
        return crime_score
    else:
        # if we don't know about the place,
        # we assume the best case and return 0
        return 0


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
        # if we don't know about the place,
        # we assume the best case and return 0
        return 0


def get_env_score(loc_data):
    env_score = {}
    aqi_score = get_aqi_score(loc_data)
    env_score['air_quality_index'] = aqi_score
    env_score['crime_rate'] = get_crime_score(loc_data)
    env_score['normalized_environment_score'] = 2 * (env_score['air_quality_index'] + env_score['crime_rate'])
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
