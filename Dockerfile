FROM python:3.9

RUN mkdir /code
WORKDIR /code
ADD / /code

RUN apt-get update

# pyBluez, gattlib の依存するライブラリをインストール
RUN apt-get install -y libbluetooth3-dev libglib2.0 libboost-python-dev libboost-thread-dev
RUN pip install -r requirements.txt

EXPOSE 5000
ENV FLASK_APP "/code/main.py"