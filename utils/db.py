import os
import requests
from pymongo.mongo_client import MongoClient
from time import time
from dotenv import load_dotenv

load_dotenv()

athlete = {'athleteID': 1}
client = MongoClient(os.environ.get('MONGODB_URI'))
tokens = None
try:
    client.admin.command('ping')
    print('Connected to MongoDB')
    tokens = client.authDB.tokens
    doc = tokens.find_one(athlete)
    os.environ['ACCESS_TOKEN'] = doc.get('accessToken')
    os.environ['EXPIRES_AT'] = doc.get('expiresAt')
except Exception as e:
    print(e)


def check_access_token() -> None:
    '''Requests and stores a new Strava API access token.'''

    if int(os.environ.get('EXPIRES_AT')) < time():
        url = 'https://www.strava.com/api/v3/oauth/token'
        params = {
            'client_id': os.environ.get('CLIENT_ID'),
            'client_secret': os.environ.get('CLIENT_SECRET'),
            'grant_type': 'refresh_token',
            'refresh_token': os.environ.get('REFRESH_TOKEN')
        }

        print('Requesting new access token...')
        post_response = requests.post(url, params=params).json()

        os.environ['ACCESS_TOKEN'] = post_response['access_token']
        os.environ['EXPIRES_AT'] = str(post_response['expires_at'])

        tokens.find_one_and_update(athlete, {
            '$set': {
                'accessToken': post_response['access_token'],
                'expiresAt': str(post_response['expires_at'])
            }
        })

        print('Access key obtained')
    return
