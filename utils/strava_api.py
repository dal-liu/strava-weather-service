import dotenv
import os
import requests
from time import time

dotenv.load_dotenv()
base_url = 'https://www.strava.com/api/v3/'


def get_latlng(id: int) -> list[int]:
    '''Returns the ending latitude and longitude of an activity.'''

    url = base_url + 'activities/' + str(id)
    
    # if access token is expired, get a new one
    if int(os.environ.get('EXPIRES_AT')) < time():
        request_access_token()
    headers = {'Authorization': 'Bearer ' + os.environ.get('ACCESS_TOKEN')}

    get_response = requests.get(url, headers=headers).json()
    return get_response.get('end_latlng', [])


def update_activity(id: int, data) -> str:
    '''Sends a PUT request and updates the activity on Strava.'''

    url = base_url + 'activities/' + str(id)
    payload = {"description": data}

    # if access token is expired, get a new one
    if int(os.environ.get('EXPIRES_AT')) < time():
        request_access_token()
    headers = {'Authorization': 'Bearer ' + os.environ.get('ACCESS_TOKEN')}

    put_response = requests.put(url, payload, headers=headers)
    # return status and reason
    return str(put_response.status_code) + ' ' + put_response.reason


def request_access_token():
    '''Requests and stores a new Strava API access token.'''

    url = base_url + 'oauth/token'
    path = os.environ.get('DOTENV_PATH')
    params = {
        'client_id': os.environ.get('CLIENT_ID'),
        'client_secret': os.environ.get('CLIENT_SECRET'),
        'grant_type': 'refresh_token',
        'refresh_token': os.environ.get('REFRESH_TOKEN')
    }

    print('Requesting new access token...')
    post_response = requests.post(url, params=params).json()
    dotenv.set_key(path, 'ACCESS_TOKEN', post_response['access_token'])
    dotenv.set_key(path, 'EXPIRES_AT', str(post_response['expires_at']))
    return
