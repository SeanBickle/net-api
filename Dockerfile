FROM python:3.9-alpine

COPY requirements.txt requirements.txt
COPY server.py server.py
COPY utils.py utils.py
COPY devices.json devices.json

RUN pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT ["python", "server.py"]
