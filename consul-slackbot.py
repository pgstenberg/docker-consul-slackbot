#!/usr/bin/env python

import sys, json, requests, os, socket

consul_data = json.loads(sys.stdin.read())

if not ('SLACK_TEAM' in os.environ and 'SLACK_TOKEN' in os.environ and 'SLACK_CHANNEL' in os.environ):
    print "Please check your environment variables."
    exit(1)

print "Team: %s" % os.environ.get('SLACK_TEAM')
print "Token: %s" % os.environ.get('SLACK_TOKEN')
print "Channel: %s" % os.environ.get('SLACK_CHANNEL')

slackbot_url = "https://%s.slack.com/services/hooks/slackbot?token=%s&channel=%s" % (str(os.environ.get('SLACK_TEAM')), str(os.environ.get('SLACK_TOKEN')), str('%23' + os.environ.get('SLACK_CHANNEL')))

pending_resolutions = []
message_pool = []

if os.path.isfile("/tmp/consul-slackbot.json"):
    with open("/tmp/consul-slackbot.json") as _file:
        pending_resolutions = json.loads(_file.read())

hostname = socket.gethostname()

def send_post(message):
    global slackbot_url
    slackbot_request = requests.post(slackbot_url, data=message)
    print(slackbot_request.status_code, slackbot_request.reason)

def add_message(message):
    if message not in message_pool:
        message_pool.append(message)

def handle_service(consul_data):
    for data_entry in consul_data:
        for check in data_entry['Checks']:
            unique_id = "%s@%s" % (check['CheckID'],data_entry['Node']['Node'])

            if(check['Status'] == 'passing' and unique_id in pending_resolutions):
                print "%s@%s=>passing:" % (check['Name'],data_entry['Node']['Node'])
                add_message("_%s_ on *%s* (%s) seams to be resolved:\n```%s```" % (check['Name'], data_entry['Node']['Node'], data_entry['Node']['Address'], check['Output']))
                pending_resolutions.remove("%s@%s" % (check['CheckID'],data_entry['Node']['Node']))

            elif(check['Status'] == 'warning' and not check['CheckID'] in pending_resolutions):
                print "%s@%s=>warning:" % (check['Name'],data_entry['Node']['Node'])
                add_message("Ups! _%s_ failed on *%s* (%s):\n```%s```" % (check['Name'], data_entry['Node']['Node'], data_entry['Node']['Address'], check['Output']))
                pending_resolutions.append(unique_id)


if os.environ.get('CONSUL_WATCH_TYPE') == 'service':
    handle_service(consul_data)

for message in message_pool:
    send_post(message)

with open("/tmp/consul-slackbot.json", "w") as _file:
    _file.write(json.dumps(pending_resolutions))
