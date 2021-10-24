import fastapi
import uvicorn

from models.text_model import TextModel
from process_doc import process_image

app = fastapi.FastAPI()


@app.get('/')
def index():
    return {
        'message': "Hello World!"
    }


@app.get('/process_image/{filename}', response_model=TextModel)
def process_img(filename: str):
    return process_image("/data/" + filename).dict()


if __name__ == '__main__':
    uvicorn.run(app)
