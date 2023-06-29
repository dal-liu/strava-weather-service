import requests_json


def get_weather_at_point(lat, lon):
    '''Takes latitude and longitude and returns a string with a brief description of the weather at that location.'''

    base_url = 'https://api.weather.gov/'

    # get the grid endpoint and nearest stations to the coordinate
    points = requests_json.get(base_url + f'points/{lat},{lon}')['properties']['observationStations']
    # get the list of nearest stations, sorted by proximity
    stations = requests_json.get(points)['observationStations']
    # get the latest observation at the nearest station
    observation = requests_json.get(stations[0] + '/observations/latest')['properties']

    # extract relevant information from response
    condition = observation['textDescription']
    temperature = round(observation['temperature']['value'] * (9/5) + 32)
    humidity = round(observation['relativeHumidity']['value'])
    wind_speed = round(observation['windSpeed']['value'] * 0.621371)
    wind_direction = get_direction(observation['windDirection']['value'])

    # return formatted string for activity description
    return f'{condition}, {temperature}ºF, Humidity {humidity}%, Wind {wind_speed}mph from {wind_direction}'


def get_direction(angle):
    '''Takes an angle from 0 to 360 and returns the associated cardinal direction.'''

    direction = None

    if 22.5 < angle <= 67.5:
        direction = 'NE'
    elif 67.5 < angle <= 112.5:
        direction = 'E'
    elif 112.5 < angle <= 157.5:
        direction = 'SE'
    elif 157.5 < angle <= 202.5:
        direction = 'S'
    elif 202.5 < angle <= 247.5:
        direction = 'SW'
    elif 247.5 < angle <= 292.5:
        direction = 'W'
    elif 292.5 < angle <= 337.5:
        direction = 'NW'
    else:
        direction = 'N'
    
    return direction
