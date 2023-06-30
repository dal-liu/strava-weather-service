import dotenv
import os
import requests
from time import time

dotenv.load_dotenv()
base_url = 'https://www.strava.com/api/v3/'


def get_lat_lon(id: int) -> list[int]:
    '''Returns the ending latitude and longitude of an activity.'''

    url = base_url + 'activities/' + str(id)
    headers = {'Authorization': 'Bearer ' + os.environ.get('ACCESS_TOKEN')}

    if int(os.environ.get('EXPIRES_AT')) < time():
        request_access_token()

    response = requests.get(url, headers=headers).json()
    return [round(n, 4) for n in response['end_latlng']]


def update_activity(id: int, data):
    '''Sends a PUT request and updates the activity on Strava.'''

    url = base_url + 'activities/' + str(id)
    payload = {"description": data}
    headers = {'Authorization': 'Bearer ' + os.environ.get('ACCESS_TOKEN')}

    if int(os.environ.get('EXPIRES_AT')) < time():
        request_access_token()

    response = requests.put(url, payload, headers=headers)
    return response.status_code


def request_access_token():
    '''Requests and stores a new Strava API access token.'''

    url = base_url + 'oauth/token'
    path = os.environ.get('PATH')
    params = {
        'client_id': os.environ.get('CLIENT_ID'),
        'client_secret': os.environ.get('CLIENT_SECRET'),
        'grant_type': 'refresh_token',
        'refresh_token': os.environ.get('REFRESH_TOKEN')
    }

    response = requests.post(url, params=params).json()
    dotenv.set_key(path, 'ACCESS_TOKEN', response['access_token'])
    dotenv.set_key(path, 'EXPIRES_AT', str(response['expires_at']))
