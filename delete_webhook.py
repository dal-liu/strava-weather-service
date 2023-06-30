import os
import requests
import sys
from dotenv import load_dotenv

if len(sys.argv) == 2:
    load_dotenv()

    url = 'https://www.strava.com/api/v3/push_subscriptions/' + sys.argv[1]
    params = {
        'client_id': os.environ.get('CLIENT_ID'),
        'client_secret': os.environ.get('CLIENT_SECRET')
    }

    response = requests.delete(url, params=params)
    print('Subscription terminated')
