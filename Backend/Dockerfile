FROM python:3
WORKDIR /main

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main/ .

EXPOSE 4100
# command to run on container start
CMD [ "python", "./server.py" ]