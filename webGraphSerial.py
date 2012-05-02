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

	usb = TeensyRawhid.Rawhid()
	usb.open(vid=int(myargs.vid,16), pid=int(myargs.pid,16))


	while running:
		time.sleep(0.001)
		try:
			txt = usb.recv(50, 100)
		except Warning:
			pass
		except IOError, e:
			print "\nUSB Error: \n%s\n" % (e)
			break
		except (KeyboardInterrupt, SystemExit):
			print '\nstopping'
			break
		print txt,
	usb.close()
	running = False

elif myargs.device_type == 'serial':
	import serial

	try: 
		ser = serial.Serial(myargs.device, myargs.baud)
		ser.open()
	except serial.SerialException, e:
		print "Could not open serial port %s: %s\n" % (myargs.device, e)
		sys.exit(1)
	
	while running:
		time.sleep(0.001)
		try:
			txt = ser.read(100)
		except OSError, e:
			print "\nSerial Error: \n%s\n" % (e)
			break
		except (KeyboardInterrupt, SystemExit):
			print '\nStopping'
			break
		print txt,
	running = False
	ser.close()




