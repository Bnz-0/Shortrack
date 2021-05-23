import sys
from common import *
import keyboard as kb
from elevate import elevate

if platform.system() != "Windows":
	elevate(graphical=True) # root permission for linux

player_addr = ('127.0.0.1',int(sys.argv[1]))
death = threading.Event()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
	s.settimeout(0.3)
	while True: # wait for the player
		try:
			s.sendto(ACK_SGN, player_addr)
			ack, addr = s.recvfrom(1)
			if addr==player_addr and ack==ACK_SGN:
				break
		except socket.timeout: pass
except Exception as e:
	log(f"waiting for the player -> {str(e)}")
	sys.exit(1)

s.settimeout(None)
del ACK_SGN

def end_of_the_fun(i):
	try:
		s.sendto(bytes([i]), player_addr)
		death.set()
	except Exception as e:
		log(f"end_of_the_fun() -> {str(e)}")

def hk_pressed(hk, i):
	try:
		s.sendto(bytes([i]), player_addr)
		while kb.is_pressed(hk): sleep(0.1)
		s.sendto(STP_SGN, player_addr)
	except Exception as e:
		log(f"hk_pressed({hk}, {i}) -> {str(e)}")

try: # bind the hotkeys
	i=0
	for _, hotkey, src in read_hk():
		if src == QUIT:
			kb.add_hotkey(hotkey, end_of_the_fun, args=[i])
		else:
			kb.add_hotkey(hotkey, hk_pressed, args=[hotkey, i])
		i+=1
except Exception as e:
	log(f"binding the hotkeys -> {str(e)}")
	sys.exit(1)

print('LISTENER READY')
death.wait()
print('LISTENER DIED')
