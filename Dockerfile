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

FROM python:alpine3.18

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["python3", "main.py"]
