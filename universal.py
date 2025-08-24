#!/usr/bin/env python3

import socket
import time
import threading
import getopt
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP

# Enable port reusage so we will be able to run multiple clients and servers on single (host, port).
# Do not use socket.SO_REUSEADDR except you using linux(kernel<3.9): goto https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ for more information.
# For linux hosts all sockets that want to share the same address and port combination must belong to processes that share the same effective user ID!
# So, on linux(kernel>=3.9) you have to run multiple servers and clients under one user to share the same (host, port).
# Thanks to @stevenreddie
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Enable broadcasting mode
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

server = False

def receive():
	print("listen thread start")
	while True:
		# Thanks @seym45 for a fix
		try:
			data, addr = client.recvfrom(1024)
			print("received message from %s: %s" % addr, data)
		except Exception:
			print("Exception occurred in receive, probably socket close")

listenThread = threading.Thread(None, receive)
try:
	if __name__ == "__main__":
	
		'''args, vals = getopt.getopt(sys.argv[1:], "s", ["server"])
		for arg, val in args:
			if arg in ("-s", "--server"):
				server = True'''
		client.bind(("", 37020))
		print("Starting")
		quit = False
		listenThread.start()
		while not quit:
			message = input().encode('utf-8')
			if(len(message) == 0):
				quit = True
			else:
				client.sendto(message, ("localhost", 37020))
				print("message sent!", flush=True)
				time.sleep(1)
except:
	print("interrupt")
finally:
	print("exiting")
	client.close()
	listenThread.join()
	quit()
