import requests

data = {}
data['gps_data'] = "50.73858,7.07873,120\n50.737204,7.102983,120"

r = requests.post("http://brma.herokuapp.com/api/v1", data)
print r.text
