'''
Created on Nov 6, 2015

@author: ankush.shah.nitk@gmail.com
'''

CRIME_MAP = None


def get_crime_rate(lat, lng):
    key = (round(lat, 1), round(lng, 1))
    crime_map = get_crime_map()

    if key in crime_map:
        n_crimes = crime_map[key]
        rate = max(min(n_crimes / 5, 100), 0)
        rate = int(rate)
        return rate
    return None


def get_crime_map():
    global CRIME_MAP
    if CRIME_MAP is None:
        CRIME_MAP = {}
        with open("data/crime_map.csv") as f:
            for line in f.readlines():
                lat, lng, n_crimes = line.split(",")
                key = (float(lat), float(lng))
                value = int(n_crimes)
                CRIME_MAP[key] = value

    return CRIME_MAP


if __name__ == "__main__":
    print get_crime_rate(26.13, -80.32)
