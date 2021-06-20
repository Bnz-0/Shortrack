import sys, threading, socket, platform
from time import sleep
import keyboard as kb
from elevate import elevate
from common import read_hk, log, ACK_SGN, STP_SGN, QUIT


def wait_for_player(soc, player_addr):
	try:
		soc.settimeout(0.3)
		while True: # wait for the player
			try:
				soc.sendto(ACK_SGN, player_addr)
				ack, addr = soc.recvfrom(1)
				if addr == player_addr and ack == ACK_SGN:
					break
			except socket.timeout: pass
	except Exception as e:
		log(f"waiting for the player -> {str(e)}")
		sys.exit(1)
	soc.settimeout(None)


def end_of_the_fun(send, death, i):
	try:
		send(bytes([i]))
		death.set()
	except Exception as e:
		log(f"end_of_the_fun() -> {str(e)}")


def hk_pressed(send, hk, i):
	try:
		send(bytes([i]))
		while kb.is_pressed(hk): sleep(0.1)
		send(STP_SGN)
	except Exception as e:
		log(f"hk_pressed({hk}, {i}) -> {str(e)}")


def main():
	if platform.system() != "Windows":
		elevate(graphical=True) # root permission for linux

	player_addr = ('127.0.0.1', int(sys.argv[1]))
	soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	wait_for_player(soc, player_addr)

	send = lambda byte: soc.sendto(byte, player_addr)
	death = threading.Event()
	try: # bind the hotkeys
		i=0
		for _, hotkey, src in read_hk():
			print(hotkey, "-->", src)
			if src == QUIT:
				kb.add_hotkey(hotkey, end_of_the_fun, args=(send, death, i))
			else:
				kb.add_hotkey(hotkey, hk_pressed, args=(send, hotkey, i))
			i+=1
	except Exception as e:
		log(f"binding the hotkeys -> {str(e)}")
		sys.exit(1)

	print('LISTENER READY')
	death.wait()
	print('LISTENER DIED')


if __name__ == "__main__":
	main()
