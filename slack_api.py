import os
import json
import requests
import urllib3
import urllib3.contrib.pyopenssl
import certifi

urllib3.contrib.pyopenssl.inject_into_urllib3()

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED', # Force certificate check.
    ca_certs=certifi.where(),  # Path to the Certifi bundle.
)

def getConfig():
    curPath = os.getcwd()
    data = []
    with open('%s/config.txt' % curPath, 'rb') as f:
        data = json.load(f)
    f.close()
    return data

def getSlackUsers():
    config = getConfig()
    
    payload = {
        'token': config['key']
    }
    r = requests.post('https://slack.com/api/users.list', params=payload)
    return  r.json()

def sendSlackMsg(receiverEmail, payload):
    payload = payload
    users = getSlackUsers()
    for user in users['members']:
#        print '*****\n' + json.dumps(user)
        try:
#            print 'wants to be: ' + receiverEmail
#            print user['profile']['email']
            if user['profile']['email'] == receiverEmail:
#                print '*****\nPosted the above\n*****'
                payload['channel'] = user['id']
        except:
            pass
    print payload
    r = requests.post('https://slack.com/api/chat.postMessage',\
                       params=payload)
    print r.status_code

if __name__ == '__main__':
    config = getConfig()
    payload = {
    'token': config['key'],
    'text': 'oh you crazy Slack APIBot',
    'username': 'BotBot'
    }
   
    sendSlackMsg(config['email'], payload)
