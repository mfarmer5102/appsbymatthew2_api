# NOTE: If installing Docker on Linux, use Snap

####################################################################
## UBUNTU 
####################################################################

#FROM ubuntu:latest
#RUN apt-get update -y

#RUN apt-get install -y \
#    python3-pip \
#    python-dev \
#    build-essential

#COPY . /app
#WORKDIR /app

#RUN pip3 install -r requirements.txt

#ENTRYPOINT ["python"]
#CMD ["main.py"]

####################################################################
## ALPINE
####################################################################

FROM alpine:latest
RUN apk add python3
RUN apk add py3-pip

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "main.py"]
