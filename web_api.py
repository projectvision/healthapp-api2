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
    if 'error' in loc_data:
        return loc_data['error']
    else:
        score = scorer.get_brma_score(loc_data)
        return json.dumps(score)


def get_loc_data(gps_data):
    loc_data = {}
    for line in gps_data.splitlines():
        if line.strip() == '':
            # empty line
            continue
        values = line.split(',')
        if len(values) != 3:
            loc_data['error'] = 'error: wrong input format'
            return loc_data
        try:
            lati, longi, time = [float(v) for v in line.split(',')]
        except ValueError:
            loc_data['error'] = 'error: wrong input values'
            return loc_data
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
