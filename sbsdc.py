#!/usr/bin/python
# # # # # # # # # # # # # # # # # # # # # # 
#
# project: Smart Bus Stops Done Dirt Cheap
# file: sbsdc.py
# description: core program for SBSDC
# language: python
# 
# authors: Anders Finn (anders@visiblethinking.com)
# date: 9/8/2012
# version: 1.1.2
# notes: for now does not do geolocation, just uses San Francisco
#
# # # # # # # # # # # # # # # # # # # # # # 

def accept_conn(data):
    references = data.split('&')
    message = ""
    sender = ""
    for x in references:
	if "body=" in x.lower():
	    message = x[5:]
	if "from=" in x.lower():
	    sender = x[8:]
    module = message.split("+")[1]
    geo = get_location(message.split("+")[0])
    message = " ".join(message.split("+")[2:])
    open(logfile, "a").write("%s: %s | %s | %s\n" % (datetime.datetime.now(), sender, module, message))
    newpid = os.fork()
    if newpid == 0:
	 run_module(module, geo , message, sender)
    else:
	 pids = (os.getpid(), newpid)     

if __name__ == "__main__":
    import sys
    import datetime
    import os
    import time
    import socket
    import threading
    from configuration import *
    
    # open port and recieve incomming connections   
    open(logfile, "a").write("\n-----------------------------------------------------\n%s: Startup, checking core and scanning modules.\n" % datetime.datetime.now())
    from modules import *
    from geocode import *
    soc = None
    backlog = 5 
    size = 1024 
    while not soc:
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	soc.bind((hostname,port)) 
	soc.listen(backlog)
	print "Server is now running"
	while 1: 
	    client, address = soc.accept() 
	    data = client.recv(size) 
	    if data: 
		accept_conn(data) 
	    client.close()
    # we should fork here??