import json
import utils.openmeteo_api as openmeteo_api
import utils.strava_api as strava_api
from flask import Flask, request, render_template
from pyngrok import ngrok

app = Flask(__name__)


if not app.debug:
    with app.app_context():
        print('Creating ngrok tunnel...')
        public_url = ngrok.connect(5000).public_url
        print(f'Callback URL: {public_url}/webhook')


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        print(f'Event update received {request.json}')
        if request.json['aspect_type'] == 'create':
            id = request.json['object_id']
            name, start_date, start_latlng = strava_api.get_name_dt_and_latlng(id)
            if len(start_latlng) == 2:
                icon, description = openmeteo_api.get_weather_at_point(start_latlng[0], start_latlng[1], start_date)
                title = icon + name
                print(f'Updating activity...')
                strava_api.update_activity(id, description, title)
            else:
                print('Activity did not contain map, did not update activity')
        else:
            print('Event was not a create, did not update activity')
        return '', 200
    elif request.method == 'GET':
        challenge = {'hub.challenge': request.args.get('hub.challenge')}
        print(f'Challenge received, sending {challenge}...')
        return json.dumps(challenge), 200
    else:
        return '', 200


if __name__ == '__main__':
    app.run()
