from evolo import *
from wifi import Cell, Scheme

parrots = scanForParrots("wlan0", [], [])

for parrot in parrots:
	print parrot.ssid, parrot.address, parrot.signal
