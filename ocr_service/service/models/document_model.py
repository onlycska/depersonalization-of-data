from typing import List

from pydantic import BaseModel

from models.text_model import TextModel


class DocumentModel(BaseModel):
    document_path: str
    temporal_files_dir: str
    num_pages: int
    pages: List[TextModel] = []
