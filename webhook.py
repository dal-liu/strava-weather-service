from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        print(request.json['aspect_type'])
        print(request.json['object_id'])
        return 'success', 200
    elif request.method == 'GET':
        challenge = {'hub.challenge': request.args.get('hub.challenge')}
        print(challenge)
        return json.dumps(challenge), 200
    else:
        return '', 200

app.run()
