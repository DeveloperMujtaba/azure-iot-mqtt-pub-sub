# https://azure.microsoft.com/en-us/documentation/articles/iot-hub-mqtt-support/
# http://stackoverflow.com/questions/35452072/python-mqtt-connection-to-azure-iot-hub/35473777
# https://azure.microsoft.com/en-us/documentation/samples/iot-hub-python-get-started/


# Mqtt Support https://www.eclipse.org/paho/clients/python/
# pip3 install paho-mqtt

# Weather data Open Weather Map using https://github.com/csparpa/pyowm
# pip3 install pyowm

import paho.mqtt.client as submqtt
import time
import helper
import sys
import json
sensor = hubAddress = deviceId = sharedAccessKey = owmApiKey = owmLocation = None

def config_load():
    global sensor, hubAddress, deviceId, sharedAccessKey, owmApiKey, owmLocation
    print('Loading default config settings')
    hubAddress = 'test-iot-hub-007.azure-devices.net'
    deviceId = 'thrust-motor'
    sharedAccessKey= 'Tn1omD5wpHfoHNCUz7M54aJoMc/WDftx+L+ypNEq0og='

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: %s" % rc)
    client.subscribe(help.hubTopicSubscribe)

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code: %s" % rc)
    client.username_pw_set(help.hubUser, help.generate_sas_token(help.endpoint, sharedAccessKey))
def on_message(client, userdata, msg):
    print("received message =", str(msg.payload.decode()))
config_load()

help = helper.Helper(hubAddress, deviceId, sharedAccessKey)

client = submqtt.Client(deviceId, submqtt.MQTTv311)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(help.hubUser, help.generate_sas_token(help.endpoint, sharedAccessKey))
#client.tls_set("/etc/ssl/certs/ca-certificates.crt") # use builtin cert on Raspbian
client.tls_set("baltimorebase64.cer") # Baltimore Cybertrust Root exported from Windows 10 using certlm.msc in base64 format
client.connect(hubAddress, 8883)
client.loop_forever()