import os
import requests as req
import json
from urllib.parse import urlencode
import datetime

sms_api_key = os.environ.get('SMS_SENDING_APK_KEY')
sms_url = os.environ.get('SMS_SENDING_URL')
sms_username = os.environ.get('SMS_SENDING_USERNAME')


def my_datetime(min_offset=0):
    now = datetime.datetime.now()
    return now + datetime.timedelta(minutes=min_offset)


def send_sms(text, dest_msisdn):
    if sms_api_key is None or sms_url is None:
        print('Missing API Key or Url')
        return None
    print(sms_api_key, sms_url, sms_username)
    data = {'username': sms_username, 'to': dest_msisdn, 'message': text}
    res = req.post(sms_url, headers={
        'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json', 'apiKey': sms_api_key}, data=urlencode(data))
    data = json.loads(res.text)
    data = data['SMSMessageData']['Recipients'][0]
    return data
