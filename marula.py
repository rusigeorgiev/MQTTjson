#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 'web listen and MQTT_publish 160601 add web.py *date* *something*.py' - proof
# of concept web listener and mqtt publisher
#
# Copyleft 2016
# The Man <rusi.georgiev@gmail.com>
# Urist McPirate <eorg.chaos@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.


# import and prepare
import paho.mqtt.publish as publish
import SocketServer
import json
import datetime
import sys
# end import and prepare


# basic variables
mqtthost = 'fisheye'
listenhost = '192.168.1.78'
listenport = 8114

# end basic variables

def pwmState (pwmValue):
  dict = {'pwmState': pwmValue}
  print "dict:", dict
  publish.single("hello/world",json.dumps(dict), hostname=mqtthost)
  print("PWM state: " + json.dumps(dict))


# do the job
def pipe_command(arg_list, standard_input=False):
    "arg_list is [command, arg1, ...], standard_input is string"
    pipe = subprocess.PIPE if standard_input else None
    subp = subprocess.Popen(arg_list, stdin=pipe, stdout=subprocess.PIPE)
    if not standard_input:
        return subp.communicate()[0]
    return subp.communicate(standard_input)[0]

class SingleTCPHandler(SocketServer.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."
    def handle(self):
        # self.request is the client connection
        pythonobj = json.loads(self.request.recv(1024))  # clip input at 1Kb
        print(pythonobj)
        self.request.close()
        try:
            if pythonobj["relayState"] == "On":
                pwmState(255)
            else:
                pwmState(0)
            # publish.single('hello/world', json.dumps(pythonobj), hostname=mqtthost)
        except IOError as err:
            print('mqtt ioerror, good luck :)', err)

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    print('server starting...'),
    server = SimpleServer((listenhost, listenport), SingleTCPHandler)
    print('started :) - exit with ctrl-c')
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nexiting now')
        sys.exit(0)
# end do the job
