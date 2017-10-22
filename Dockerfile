FROM ubuntu:16.04
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /summaggle_sourcerer
WORKDIR /summaggle_sourcerer
RUN pip install -r requirements.txt
ENTRYPOINT ["make"]
CMD ["start-web"]
