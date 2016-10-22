import paho.mqtt.publish as publish
import time
import json
print("Sending 0...")
dict = {'relayState': 'On'}
##publish.single(json.dumps(dict))
publish.single("hello/world",json.dumps(dict), hostname="fisheye")

print("Relay state: " +json.dumps(dict))
time.sleep(1)
##publish.single("hello/world", "1", hostname="127.0.0.1")
dict = {'relayState': 'Off'}
##publish.single(json.dumps(dict))
publish.single("hello/world",json.dumps(dict), hostname="fisheye")
print("Relay state: " +json.dumps(dict))
