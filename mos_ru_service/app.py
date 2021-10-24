import json

from flask import Flask, render_template, redirect, request, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

import os
import logging
import requests

UPLOAD_FOLDER = './uploaded'
OCR_ADDRESS = r'http://ocr:80/process_image/'
NER_ADDRESS = r'http://ner:5001/api/extract-personal-data'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

logs_folder_path = os.path.join(os.getcwd(), 'logs')
os.makedirs(logs_folder_path, exist_ok=True)
log_path = os.path.join(f'{logs_folder_path}', f'{datetime.date(datetime.now())}.log')
logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG,
                    filename=log_path,
                    filemode='a',
                    datefmt='%d-%b-%y %H:%M:%S')

bootstrap = Bootstrap(app)
moment = Moment(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files.get('file', None)
        if file is None:
            flash('No file part')
            logging.error('Request received without file part.')
            return redirect(request.url)
        # Если пользователь не выбирает файл, браузер отправляет пустой файл без имени.
        if file.filename == '':
            flash('No selected file')
            logging.error('Request received without selected file.')
            return redirect(request.url)
        _, file_ext = os.path.splitext(file.filename)
        filename = datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f") + file_ext
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        logging.debug('File successfuly uploaded.')
        req = requests.get(OCR_ADDRESS + filename)
        text = req.json().get('text')
        text = json.dumps(text, ensure_ascii=False)
        text = ' '.join(text)
        data = {'text': text}
        r = requests.get(NER_ADDRESS, data=data)
        flash(r.text)
        return render_template('index.html')
    except Exception as e:
        logging.error(f'Error occured: {e}', exc_info=True)
        internal_server_error(e)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
