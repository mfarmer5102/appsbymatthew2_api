# NOTE: If installing Docker on Linux, use Snap

FROM ubuntu:latest
RUN apt-get update -y

RUN apt-get install -y \
    python3-pip \
    python-dev \
    build-essential

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install flask
RUN pip3 install pymongo
RUN pip3 python-dotenv
RUN pip3 install dnspython
RUN pip3 install flask_cors

ENTRYPOINT ["python"]

CMD ["main.py"]
