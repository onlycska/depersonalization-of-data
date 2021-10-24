import time
import fastapi
import uvicorn
import logging
import os

from process_doc import process_image
from models.document_model import DocumentModel
from pdf2jpg import pdf2jpg
from datetime import datetime

logs_folder_path = os.path.join(os.getcwd(), 'logs')
os.makedirs(logs_folder_path, exist_ok=True)
log_path = os.path.join(f'{logs_folder_path}', f'{datetime.date(datetime.now())}.log')
logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG,
                    filename=log_path,
                    filemode='a',
                    datefmt='%d-%b-%y %H:%M:%S')

app = fastapi.FastAPI()


@app.get('/')
def index():
    return {
        'message': "Hello World!"
    }


@app.get('/process_doc/{filename}', response_model=DocumentModel)
def process_doc(filename: str):
    file_extension = filename.split('.')[-1]
    if file_extension == "pdf":
        return process_pdf(filename)
    elif file_extension == "jpg" \
            or file_extension == "jpeg" \
            or file_extension == "png":
        return process_img(filename)


def process_pdf(filename: str):
    pages_paths = pdf2jpg(filename)
    pages = []
    for page_path in pages_paths:
        pages.append(process_image(page_path))

    result = {
        "document_path": filename,
        "temporal_files_dir": f"/data/converted/{filename.split('.')[-2]}",
        "num_pages": len(pages),
        "pages": pages
    }
    return DocumentModel(**result).dict()


def process_img(filename: str):
    try:
        filepath =  '/data/' + filename
        for i in range(10):
            if os.path.exists(filepath):
                break
            time.sleep(1)
        result = {
            "document_path": filename,
            "temporal_files_dir": "",
            "num_pages": 1,
            "pages": [process_image("/data/" + filename)]
        }
        return DocumentModel(**result).dict()
    except Exception as e:
        logging.error(f'Error occured: {e}', exc_info=True)
        return {
            'message': 'Error occured, see logs for details.'
        }


if __name__ == '__main__':
    uvicorn.run(app)
