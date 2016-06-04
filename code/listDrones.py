from wifi import Cell, Scheme
from main import interfaceForScan
from evolo import scanForParrots, disconnectFromWifi

disconnectFromWifi(interfaceForScan)
parrots = scanForParrots(interfaceForScan, [], [])

for parrot in parrots:
	print "listDrones;" + parrot.ssid + ";" + parrot.address + ";" + str(parrot.signal)
