import requests


def get_weather_at_point(lat: int, lon: int) -> str:
    '''Takes latitude and longitude and returns a string with a brief description of the weather at that location.'''

    base_url = 'https://api.weather.gov/'

    # round lat and lon to 4 decimal digits
    lat, lon = round(lat, 4), round(lon, 4)

    # get the grid endpoint and nearest stations to the coordinate
    points = requests.get(base_url + f'points/{lat},{lon}').json()['properties']['observationStations']
    # get the list of nearest stations, sorted by proximity
    stations = requests.get(points).json()['observationStations']
    # get the latest observation at the nearest station
    observation = requests.get(stations[0] + '/observations/latest').json()['properties']

    # extract relevant information from response
    condition = get_condition(observation['textDescription'])
    temperature = round(observation['temperature']['value'] * (9/5) + 32)
    humidity = round(observation['relativeHumidity']['value'])
    wind_speed = get_wind_speed(observation['windSpeed']['value'])
    wind_direction = get_wind_direction(observation['windDirection']['value'], wind_speed)

    # return formatted string for activity description
    return f'{condition}{temperature}ºF, Humidity {humidity}%, Wind {wind_speed}mph {wind_direction}'


def get_condition(condition) -> str:
    '''If condition is N/A, then returns an empty string.'''
    
    return condition + ', ' if condition else ''


def get_wind_speed(wind_speed) -> int:
    '''Returns wind speed in mph. If wind is unavailable, returns 0.'''
    
    return round(wind_speed * 0.621371) if wind_speed else 0


def get_wind_direction(angle, speed) -> str:
    '''Takes an angle from 0 to 360 and returns the associated cardinal direction.'''

    if not speed:
        return ''
    if not angle:
        return 'from N'
    
    direction = 'from '

    if 22.5 < angle <= 67.5:
        direction += 'NE'
    elif 67.5 < angle <= 112.5:
        direction += 'E'
    elif 112.5 < angle <= 157.5:
        direction += 'SE'
    elif 157.5 < angle <= 202.5:
        direction += 'S'
    elif 202.5 < angle <= 247.5:
        direction += 'SW'
    elif 247.5 < angle <= 292.5:
        direction += 'W'
    elif 292.5 < angle <= 337.5:
        direction += 'NW'
    else:
        direction += 'N'
    
    return direction
