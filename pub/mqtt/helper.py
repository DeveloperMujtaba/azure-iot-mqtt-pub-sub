# Python 2.7 Sas generator https://azure.microsoft.com/en-us/documentation/articles/iot-hub-sas-tokens/#comments/

import base64
import hmac
import urllib.parse
import time

class Helper():

    hubAddress, hubName, SharedAccessKey = ['','','']

    endpoint, hubUser, hubTopicPublish, hubTopicSubscribe = ['','','','']

    def __init__(self, hubAddress, hubName, SharedAccessKey):
        self.hubAddress = hubAddress
        self.hubName = hubName
        self.SharedAccessKey = SharedAccessKey

        self.endpoint = hubAddress + '/devices/' + hubName
        self.hubUser = hubAddress + '/' + hubName
        self.hubTopicPublish = 'devices/' + hubName + '/messages/events/'
        self.hubTopicSubscribe = 'devices/' + hubName + '/messages/#'


    # sas generator from https://github.com/bechynsky/AzureIoTDeviceClientPY/blob/master/DeviceClient.py
    def generate_sas_token(self, uri, key, expiry=3600):
        ttl = int(time.time()) + expiry
        urlToSign = urllib.parse.quote(uri, safe='') 
        sign_key = "%s\n%d" % (urlToSign, int(ttl))
        h = hmac.new(base64.b64decode(key), msg = "{0}\n{1}".format(urlToSign, ttl).encode('utf-8'),digestmod = 'sha256')
        signature = urllib.parse.quote(base64.b64encode(h.digest()), safe = '')
        return "SharedAccessSignature sr={0}&sig={1}&se={2}".format(urlToSign, urllib.parse.quote(base64.b64encode(h.digest()), safe = ''), ttl)
