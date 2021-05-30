FROM python:3.9

RUN mkdir /code
WORKDIR /code
ADD / /code

RUN apt-get update

# bluetoothの依存するライブラリをインストール
RUN apt-get install -y python-dev libbluetooth-dev libboost-all-dev
RUN pip install -r requirements.txt

EXPOSE 5000
ENV FLASK_APP "/code/main.py"