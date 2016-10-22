import paho.mqtt.publish as publish
import time
import json
print("Sending 0...")

def pwmState (pwmValue):
  dict = {'pwmState': pwmValue}
  print "dict:", dict
  publish.single("hello/world",json.dumps(dict), hostname="fisheye")
  print("PWM state: " + json.dumps(dict))

def relayStateSwitch (onOff):
  dict = {'relayState': 'On'}
  publish.single("hello/world",json.dumps(dict), hostname="fisheye")
  print("Relay state: " + json.dumps(dict))
  time.sleep(1)
  dict = {'relayState': 'Off'}
  publish.single("hello/world",json.dumps(dict), hostname="fisheye")
  print("Relay state: " + json.dumps(dict))


for ii in range(256):
  print ii
  time.sleep(0.01)
  pwmState(ii)
  

##pwmState(10)
##time.sleep(1)
##pwmState(30)
##time.sleep(1)
##pwmState(50)
##time.sleep(1)
##pwmState(70)
##time.sleep(1)
##pwmState(100)
##time.sleep(1)
##pwmState(255)
time.sleep(5)
pwmState(0)
##
