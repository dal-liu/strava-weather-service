import os
import requests
import sys
from dotenv import load_dotenv

if len(sys.argv) == 2:
    load_dotenv()
    
    url = 'https://www.strava.com/api/v3/push_subscriptions'
    params = {
        'client_id': os.environ.get('CLIENT_ID'),
        'client_secret': os.environ.get('CLIENT_SECRET'),
        'callback_url': sys.argv[1],
        'verify_token': 'STRAVA'
    }

    response = requests.post(url, params=params)
    print(f'Subscription ID: {response.json()["id"]}')
