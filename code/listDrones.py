from wifi import Cell, Scheme
from main import interfaceForScan
from evolo import scanForParrots

parrots = scanForParrots(interfaceForScan, [], [])

for parrot in parrots:
	print "listDrones;" + parrot.ssid + ";" + parrot.address + ";" + str(parrot.signal)
