'''
* Copyright ProjectVisionHealth (c) 2015
* Author Name: Ankush Shah
* Date : 22 Dec 2015
* Description: Module for providing the crime rate api
'''

CRIME_MAP = None
CRIME_SCALE = 5


def get_crime_rate(lat, lng):
    key = (round(lat, 1), round(lng, 1))
    crime_map = get_crime_map()
    crime_rate = None
    if key in crime_map:
        n_crimes = crime_map[key]
        crime_rate = max(min(n_crimes / CRIME_SCALE, 100), 0)
        crime_rate = int(crime_rate)
    return crime_rate


def get_crime_map():
    global CRIME_MAP
    if CRIME_MAP is None:
        CRIME_MAP = {}
        # csv containing latitude, longitude and no_of_crimes
        with open("data/crime_map.csv") as f:
            for line in f.readlines():
                lat, lng, n_crimes = line.split(",")
                key = (float(lat), float(lng))
                value = int(n_crimes)
                CRIME_MAP[key] = value

    return CRIME_MAP


if __name__ == "__main__":
    print get_crime_rate(26.13, -80.32)
