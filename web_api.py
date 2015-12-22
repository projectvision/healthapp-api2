'''
Created on Nov 13, 2015

@author: ankush.shah.nitk@gmail.com
'''

import os
import json
from flask import Flask, request, render_template, jsonify
import scorer

app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('input.html')


@app.route('/api/v1', methods=['GET', 'POST'])
def api():
    if 'gps_data' in request.form:
        gps_data = request.form['gps_data']
    else:
        return 'error: gps_data not found'
    loc_data = get_loc_data(gps_data)
    if 'projectvision_error_code' in loc_data:
        return json.dumps(loc_data)
    else:
        score = scorer.get_brma_score(loc_data)
        return json.dumps(score)


def get_loc_data(gps_data):
    loc_data = {}
    try:
        gps_data = json.loads(gps_data)
    except ValueError:
        loc_data["projectvision_error_code"] = 100
        loc_data["error_desc"] = "invalid json: %s" % gps_data
        return loc_data

    for loc in gps_data["location"]:
        if "latitude" in loc:
            try:
                lati = float(loc["latitude"])
            except ValueError:
                loc_data["projectvision_error_code"] = 101
                loc_data["error_desc"] = "invalid value for latitude: %s" % loc["latitude"]
                return loc_data
        else:
            loc_data["projectvision_error_code"] = 102
            loc_data["error_desc"] = "missing value for latitude in %s" % loc
            return loc_data

        if "longitude" in loc:
            try:
                longi = float(loc["longitude"])
            except ValueError:
                loc_data["projectvision_error_code"] = 101
                loc_data["error_desc"] = "invalid value for longitude: %s" % loc["longitude"]
                return loc_data
        else:
            loc_data["projectvision_error_code"] = 102
            loc_data["error_desc"] = "missing value for longitude in %s" % loc
            return loc_data

        if "duration" in loc:
            try:
                time = float(loc["duration"])
            except ValueError:
                loc_data["projectvision_error_code"] = 101
                loc_data["error_desc"] = "invalid value for duration: %s" % loc["duration"]
                return loc_data
        else:
            loc_data["projectvision_error_code"] = 102
            loc_data["error_desc"] = "missing value for duration in %s" % loc
            return loc_data

        # at this point data is completely checked
        key = (lati, longi)
        if key in loc_data:
            loc_data[key] += time
        else:
            loc_data[key] = time

    return loc_data

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

# sample data to post
# 50.73858,7.07873,120 (McFit)
# 50.737204,7.102983,120 (Subway)

# 37.757815,-122.5076408,120 #SF
# 40.7058316,-74.2582003,120 #New York
