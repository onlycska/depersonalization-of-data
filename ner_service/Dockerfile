FROM python:3.7 AS base
WORKDIR /usr/src/ner_service
EXPOSE 5001
ADD . .
RUN pip install -r requirements.txt && \
    python -m deeppavlov install ner_rus && \
    python -m deeppavlov download ner_rus
ENTRYPOINT ["python3", "app.py"]