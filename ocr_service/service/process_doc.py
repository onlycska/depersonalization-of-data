import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from models.text_model import TextModel

# Tesseract Library
import pytesseract
from pytesseract import Output

import cv2


def draw_bboxes(doc: pd.DataFrame, img: np.ndarray):
    d = doc.to_dict('list')
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        if (d['conf'][i] != '-1') and len(d['text'][i].split(' ')) == 1:
            (x, y, w, h) = (int(d['left'][i]), int(d['top'][i]), int(d['width'][i]), int(d['height'][i]))
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imwrite("../example.png", img)


def process_image(image_path: str):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    df = pytesseract.image_to_data(image, lang='rus', output_type=Output.DATAFRAME).dropna()
    df = df.where(df['conf'] != '-1').dropna()

    blocks = df.drop_duplicates(subset=['block_num'])['block_num'].tolist()
    text = ""
    boxes_map = []
    for block in blocks:
        block_df = df.where(df['block_num'] == block).dropna()
        block_words = block_df['text'].tolist()
        block_words_lines = block_df['line_num'].tolist()
        curr_lnum = block_words_lines[0]
        for word, line in zip(block_words, block_words_lines):
            boxes_map.append(len(text))
            if line != curr_lnum:
                text += "\n"
                curr_lnum = line
            else:
                text += " "
            text += word
        text += "\n\n"

    x_top_left = [int(x) for x in df['left'].tolist()]
    y_top_left = [int(y) for y in df['top'].tolist()]
    x_bottom_right = [x + int(w) for x, w in zip(x_top_left, df['width'].tolist())]
    y_bottom_right = [y + int(h) for y, h in zip(y_top_left, df['height'].tolist())]

    draw_bboxes(df, image)
    result = {
        "image_path": image_path,
        "text": text,
        "boxes_map": boxes_map,
        "b_boxes_x_tl": x_top_left,
        "b_boxes_y_tl": y_top_left,
        "b_boxes_x_br": x_bottom_right,
        "b_boxes_y_br": y_bottom_right,
    }
    return TextModel(**result)
