import json

from flask import Flask, request
from flask import jsonify
from flask import request
from makeMelody.melodyModel import MelodyModel
from configuration.constant import MODEL_DESCRIPTION
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'*': {'origins': 'http://localhost:8080'}})
model = MelodyModel(MODEL_DESCRIPTION)


@app.route('/')
def hello():
    return 'Hello gunwoong World!'


@app.route('/getMelody/<username>', methods=['GET'])
def makeMelody(username):
    json_data = request.form.get('inputs', '')

    try:
        json_data = json.loads(json_data)
        user_id_data = json_data.get('userId', "unknown")
        texts_data = json_data.get('texts', [])
        token_cnt = json_data.get('token_cnt', 256)
        youtube_uri_data = json_data.get('youtube_uri', [])

    except json.JSONDecodeError as e:
        print("gwj : Json error")

    model.upload_to_s3(texts_data, token_cnt,user_id_data,'wav')

    response = {'status': 'success', 'message': 'received successfully'}
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
