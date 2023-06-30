import json
import strava_api
from flask import Flask, request
from noaa_weather import get_weather_at_point

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        print(request.json)
        if request.json['aspect_type'] == 'create':
            id = request.json['object_id']
            end_latlng = strava_api.get_latlng(id)
            if len(end_latlng) == 2:
                description = get_weather_at_point(end_latlng[0], end_latlng[1])
                put_response = strava_api.update_activity(id, description)
                print(put_response)
        return 'success', 200
    elif request.method == 'GET':
        challenge = {'hub.challenge': request.args.get('hub.challenge')}
        print(challenge)
        return json.dumps(challenge), 200
    else:
        return '', 200

app.run()
