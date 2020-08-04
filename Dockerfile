# NOTE: If installing Docker on Linux, use Snap

FROM ubuntu:18.04
RUN apt-get update -y

RUN apt-get install -y \
    python3-pip \
    python-dev \
    build-essential

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt
ENTRYPOINT ["python"]

CMD ["server.py"]
