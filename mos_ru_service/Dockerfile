FROM python:3.9 AS base
WORKDIR /usr/src/mos_ru_service
EXPOSE 5000
ADD . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]