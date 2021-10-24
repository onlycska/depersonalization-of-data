from typing import List

from pydantic import BaseModel


class TextModel(BaseModel):
    image_path: str
    text: str
    b_boxes_x_tl: List[int] = []
    b_boxes_y_tl: List[int] = []
    b_boxes_x_br: List[int] = []
    b_boxes_y_br: List[int] = []
