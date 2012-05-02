from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import mimetypes
readDataFn = 0


class httpHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			if self.path == "/data":
				self.send_response(200)
				self.send_header('Content-Type',	'text/event-stream')
				self.end_headers()
				i=0
				while(True):
					try:
						self.wfile.write("data: " + readDataFn() + "\n\n")
						#time.sleep(1)
						i += 1
					except KeyboardInterrupt:
						break
				return
			try:
				fi = open(curdir + self.path, 'rb')
				self.send_response(200)
				self.send_header('Content-Type',	mimetypes.guess_type(self.path)[0] )
				self.end_headers()
				self.wfile.write( fi.read() )

			except IOError:
				self.send_error(404,'File Not Found: %s' % self.path)
				return
			
		except IOError:
			self.send_error(404,'File Noooot Found: %s' % self.path)		


if __name__ == '__main__':
	import argparse
	import time, sys
	parser = argparse.ArgumentParser(description='webGraphSerial commandline options')
	#protos = parser.add_mutually_exclusive_group()
	subparsers = parser.add_subparsers(dest="device_type", help='Device type to connect to')

	usb_parser = subparsers.add_parser('usb', help='Use a USB HID device')
	usb_parser.add_argument('vid', action='store', default=0xE413, help='Vendor ID to connect to')
	usb_parser.add_argument('pid', action='store', default=0xBEEF, help='Device id to connect to')

	ser_parser = subparsers.add_parser('serial', help='Use a Serial TTY device')
	ser_parser.add_argument('device', action='store', help='Device (in /dev/ or COM*)')
	ser_parser.add_argument('baud', action='store', default=115200, type=int, help='Serial Baud Rate to use')

	myargs = parser.parse_args()
	running = True

	if myargs.device_type == 'usb':
		import TeensyRawhid

		connect = TeensyRawhid.Rawhid()
		connect.open(vid=int(myargs.vid,16), pid=int(myargs.pid,16))
		
		def readConnection():
			try:
				return connect.recv(50, 1000) #(buff size, timeout)
			except Warning:
				pass
		#connect.close()

	elif myargs.device_type == 'serial':
		import serial

		connect = serial.Serial(myargs.device, myargs.baud)
		connect.open()
		
		def readConnection():
			try:
				return connect.read(100)
			except OSError, e:
				raise IOError(e)
		#connect.close()
	global readDataFn
	readDataFn = readConnection

	try:
		server = HTTPServer(('', 8080), httpHandler)
		print 'started httpserver...'
		server.serve_forever()
	except KeyboardInterrupt:
		print '^C received, shutting down server'
		server.socket.close()

