import os
from time import time

import requests
from pymongo.mongo_client import MongoClient

athlete = {"athleteID": 1}
client = MongoClient(os.environ.get("MONGODB_URI"))
tokens = None
activities = None
try:
    client.admin.command("ping")
    print("Connected to MongoDB")
    tokens = client.authDB.tokens
    activities = client.activityDB.activities
    doc = tokens.find_one(athlete)
    if doc:
        os.environ["ACCESS_TOKEN"] = doc.get("accessToken")
        os.environ["EXPIRES_AT"] = doc.get("expiresAt")
except Exception as e:
    print(e)


def check_access_token() -> None:
    """Requests and stores a new Strava API access token."""

    expires_at = os.environ.get("EXPIRES_AT")
    if not expires_at or int(expires_at) < time():
        url = "https://www.strava.com/api/v3/oauth/token"
        params = {
            "client_id": os.environ.get("CLIENT_ID"),
            "client_secret": os.environ.get("CLIENT_SECRET"),
            "grant_type": "refresh_token",
            "refresh_token": os.environ.get("REFRESH_TOKEN"),
        }

        print("Requesting new access token...")
        post_response = requests.post(url, params=params).json()

        os.environ["ACCESS_TOKEN"] = post_response["access_token"]
        os.environ["EXPIRES_AT"] = str(post_response["expires_at"])

        if tokens is not None:
            tokens.find_one_and_update(
                athlete,
                {
                    "$set": {
                        "accessToken": post_response["access_token"],
                        "expiresAt": str(post_response["expires_at"]),
                    }
                },
            )

            print("Access key obtained")


def is_new_activity(id: int) -> bool:
    """Checks if the activity has been seen before."""

    if activities is not None:
        doc = activities.find_one({"activityID": id})
        if not doc:
            activities.insert_one({"activityID": id})
            return True
    return False
