FROM python:3.7 AS base
WORKDIR /usr/src/ner-service
EXPOSE 5000
ADD . .
RUN pip install -r requirements.txt && \
    rm -r ./logs && \
    python -m deeppavlov install ner_rus && \
    python -m deeppavlov download ner_rus
ENTRYPOINT ["python3", "app.py"]