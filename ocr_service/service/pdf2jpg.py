from pdf2image import convert_from_path
from pathlib import Path


def check_dir(dirname: str):
    Path(dirname).mkdir(parents=True, exist_ok=True)


def pdf2jpg(filename: str):
    pages = convert_from_path(f"/data/{filename}", 600)
    converted_pages = []
    temp_dir = f"/data/converted/{filename.split('.')[-2]}"
    check_dir(temp_dir)
    for idx, page in enumerate(pages):
        page_path = temp_dir + f"/page_{idx}.jpg"
        page.save(page_path, 'JPEG')
        converted_pages.append(page_path)

    return converted_pages
