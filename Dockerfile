FROM python:2-wheezy

RUN apt-get update && apt-get install -y unzip
ADD https://dl.bintray.com/mitchellh/consul/0.5.2_linux_amd64.zip /tmp/consul.zip
RUN cd /bin && unzip /tmp/consul.zip && chmod +x /bin/consul && rm /tmp/consul.zip

COPY slackbot.py /bin/watch-slackbot

RUN pip install requests

ENTRYPOINT ["consul","watch","-http-addr=192.168.1.150:8500","-type=service","-service=devservice","watch-slackbot"]
