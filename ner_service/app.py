import os.path

import flask

from os import getcwd
from datetime import datetime
from ner import predict_ner

import logging

app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

logs_folder_path = os.path.join(getcwd(), 'logs')
os.makedirs(logs_folder_path, exist_ok=True)
log_path = os.path.join(f'{logs_folder_path}', f'{datetime.date(datetime.now())}.log')
logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG,
                    filename=log_path,
                    filemode='a',
                    datefmt='%d-%b-%y %H:%M:%S')
logging.getLogger('deeppavlov').setLevel(logging.ERROR)
logging.getLogger('tensorflow').setLevel(logging.ERROR)


@app.route('/api/extract-personal-data', methods=['GET'])
def extract_personal_data() -> flask.Response:
    logging.debug(f'The request was received to search for NER tags.')
    answer = {}
    try:
        request_data = flask.jsonify(flask.request.form).json
        text = request_data.get('text', '')
        if not text:
            answer['message'] = 'The text was not passed to the api method.'
            return flask.make_response(flask.jsonify(answer), 400)
        predicted_ner = predict_ner(text)
        answer['message'] = predicted_ner
        return flask.make_response(flask.jsonify(answer), 200)

    except Exception as e:
        logging.exception(e)
        return flask.jsonify(flask.Response(f'Some error occured: {e}', 500))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
