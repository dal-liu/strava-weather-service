import os
import requests
from dotenv import load_dotenv

load_dotenv()
base_url = 'https://www.strava.com/api/v3/push_subscriptions'


def create(callback_url: str) -> int:
    params = {
        'client_id': os.environ.get('CLIENT_ID'),
        'client_secret': os.environ.get('CLIENT_SECRET'),
        'callback_url': callback_url,
        'verify_token': 'STRAVA'
    }

    print('Creating webhook subscription...')
    response = requests.post(base_url, params=params).json()
    print(response)
    return response['id']


def delete(id: int):
    url = base_url + str(id)
    params = {
        'client_id': os.environ.get('CLIENT_ID'),
        'client_secret': os.environ.get('CLIENT_SECRET')
    }

    print('Deleting webhook subscription...')
    response = requests.delete(url, params=params)
    if response.status_code == 204:
        print('Subscription deleted')
    else:
        print(f'Error deleting subscription: {response.status_code} {response.content}')
    return
