import os

import requests

base_url = "https://www.strava.com/api/v3/"


def get_name_dt_and_latlng(id: int):
    """Returns the ending latitude and longitude and the datetime of an activity."""

    url = base_url + "activities/" + str(id)
    headers = {"Authorization": f"Bearer {os.environ.get("ACCESS_TOKEN")}"}

    print("Getting map data...")
    get_response = requests.get(url, headers=headers).json()
    return (
        get_response.get("name"),
        get_response.get("start_date"),
        get_response.get("start_latlng"),
    )


def update_activity(id: int, description: str, title: str):
    """Sends a PUT request and updates the activity on Strava."""

    url = base_url + "activities/" + str(id)
    payload = {"description": description, "name": title}
    headers = {"Authorization": f"Bearer {os.environ.get("ACCESS_TOKEN")}"}

    put_response = requests.put(url, payload, headers=headers)
    # print status and reason
    print("Status: " + str(put_response.status_code) + " " + put_response.reason)
