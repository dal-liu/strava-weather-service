import json

from flask import Flask, render_template, request

import utils.db as db
import utils.openmeteo_api as openmeteo_api
import utils.strava_api as strava_api

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("./index.html")


@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    if request.method == "POST":
        print(f"Event update received {request.json}")

        if (
            not request.json
            or request.json["aspect_type"] != "create"
            or not db.is_new_activity(request.json["object_id"])
        ):
            print("Event was not a new create, did not update activity")
            return "", 200

        id = request.json["object_id"]
        db.check_access_token()
        name, start_date, start_latlng = strava_api.get_name_dt_and_latlng(id)

        if len(start_latlng) != 2:
            print("Activity did not contain map, did not update activity")
            return "", 200

        icon, description = openmeteo_api.get_weather_at_point(
            start_latlng[0], start_latlng[1], start_date
        )

        if not icon or not description:
            print("Weather API error, did not update activity")
            return "", 200

        title = icon + name
        print(f"Updating activity...")
        db.check_access_token()
        strava_api.update_activity(id, description, title)
        return "", 200
    elif request.method == "GET":
        challenge = {"hub.challenge": request.args.get("hub.challenge")}
        print(f"Challenge received, sending {challenge}...")
        return json.dumps(challenge), 200
    else:
        return "", 200


if __name__ == "__main__":
    app.run()
