docker run \
  -p 8000:80 \
  -v /home/kowalski/Downloads/ilovepdf_pages-to-jpg/:/data/:rw \
  --name ocr-doc-process \
  50d7c79d6fd6