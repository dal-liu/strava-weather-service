from noaa_weather import get_weather_at_point
import strava
import json


if __name__ == '__main__':
    f = open('./sample.json')    
    data = json.load(f)
    print(data['end_latlng'])
    latlng = [round(x, 4) for x in data['end_latlng']]
    print(get_weather_at_point(latlng[0], latlng[1]))
