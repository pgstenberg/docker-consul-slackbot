FROM python:2-wheezy

RUN apt-get update && apt-get install -y unzip
ADD https://dl.bintray.com/mitchellh/consul/0.5.2_linux_amd64.zip /tmp/consul.zip
RUN cd /bin && unzip /tmp/consul.zip && chmod +x /bin/consul && rm /tmp/consul.zip

COPY consul-slackbot.py /bin/consul-slackbot.py
COPY consul-slackbot.sh /bin/consul-slackbot.sh

RUN chmod +x /bin/consul-slackbot.py && chmod +x /bin/consul-slackbot.sh

RUN pip install requests

ENTRYPOINT ["/bin/consul-slackbot.sh"]
