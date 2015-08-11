#!/usr/bin/env python

import sys, json, requests, os, socket

consul_data = json.loads(sys.stdin.read())

print "Team: %s" % os.environ.get('SLACK_TEAM')
print "Token: %s" % os.environ.get('SLACK_TOKEN')
print "Channel: %s" % os.environ.get('SLACK_CHANNEL')

slackbot_url = "https://%s.slack.com/services/hooks/slackbot?token=%s&channel=%s" % (str(os.environ.get('SLACK_TEAM')), str(os.environ.get('SLACK_TOKEN')), str('%23' + os.environ.get('SLACK_CHANNEL')))

pending_resolutions = []
hostname = socket.gethostname()

def send_post(message):
    global slackbot_url
    slackbot_request = requests.post(slackbot_url, data=message)
    print(slackbot_request.status_code, slackbot_request.reason)


for data_entry in consul_data:
    for check in data_entry['Checks']:
        if(check['Status'] == 'passing' and check['CheckID'] in pending_resolutions):
            slackbot_message = "%s:_%s_ seams on *%s* (%s) to be resolved:\n```%s```" % (hostname, check['Name'], data_entry['Node']['Node'], data_entry['Node']['Address'], check['Output'])
            print "%s@%s=>passing:" % (check['Name'],data_entry['Node']['Node'])
            send_post(slackbot_message)
            pending_resolutions.remove("%s@%s" % (check['CheckID'],data_entry['Node']['Node']))

        elif(check['Status'] == 'warning' and not check['CheckID'] in pending_resolutions):
            slackbot_message = "%s:Ups! _%s_ failed on *%s* (%s):\n```%s```" % (hostname, check['Name'], data_entry['Node']['Node'], data_entry['Node']['Address'], check['Output'])
            print "%s@%s=>warning:" % (check['Name'],data_entry['Node']['Node'])
            send_post(slackbot_message)
            pending_resolutions.append("%s@%s" % (check['CheckID'],data_entry['Node']['Node']))


print (pending_resolutions)
