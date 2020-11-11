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
RUN pip3 install flask 1.1.1
RUN pip3 install 3.9.0
RUN pip3 python-dotenv 0.12.0
RUN pip3 install dnspython 1.16.0
RUN pip3 install flask_cors 3.0.8

ENTRYPOINT ["python"]

CMD ["main.py"]
