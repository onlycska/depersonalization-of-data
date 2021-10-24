FROM tesseractshadow/tesseract4re
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update -y && apt upgrade -y
RUN apt install -y -q build-essential python3-pip python3-dev python3-opencv poppler-utils
RUN pip3 install -U pip setuptools wheel
RUN pip3 install gunicorn uvloop httptools
COPY requirments.txt /app/requirments.txt
RUN pip3 install -r /app/requirments.txt
COPY service/ /app

ENTRYPOINT /usr/local/bin/gunicorn \
    -b 0.0.0.0:80 \
    -k uvicorn.workers.UvicornWorker \
    --chdir /app main:app