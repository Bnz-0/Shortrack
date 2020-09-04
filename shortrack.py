#!/bin/env python3
from common import *
import pyaudio, wave

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1',0))
os.spawnlp(os.P_NOWAIT, # spawn the listener
	sys.executable, sys.executable,
	os.path.dirname(os.path.abspath(__file__))+'/hk_listener.py', str(s.getsockname()[1])
)
HKLIST = read_hk()
p = pyaudio.PyAudio()
listener_addr = None
stop=False

def play(hotkey, src):
	try:
		with wave.open(PATH+src, 'rb') as wf:
			data = None
			stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
							channels=wf.getnchannels(),
							rate=wf.getframerate(),
							output=True)
			while not stop and data != b'':
				data = wf.readframes(1024)
				stream.write(data)
			stream.stop_stream()
			stream.close()
	except Exception as e:
		log(f"play({src}, {hotkey}) -> {str(e)}")

ack = None
try: # wait for the listener
	while ack != ACK_SGN:
		ack, listener_addr = s.recvfrom(1)
		s.sendto(ACK_SGN, listener_addr)
except Exception as e:
		log(f"waiting for the listener (recv={ack}, addr={listener_addr}) -> {str(e)}")
		exit(1)
del ack, ACK_SGN
print('PLAYER READY')

r = player = None
while True:
	try:
		r, addr = s.recvfrom(1)
		print('PLAYER recv', r, addr)
		if addr != listener_addr: continue
		elif r == STP_SGN:
			stop=True
			if player is not None:
				player.join()
		elif HKLIST[r[0]][1] == 'QUIT': break
		else:
			stop=False
			player = threading.Thread(target=play, args=HKLIST[r[0]])
			player.start()
	except Exception as e:
			log(f"listening for hotkeys (recv={r}, addr={addr}, listener_addr={listener_addr}) -> {str(e)}")

p.terminate()
s.close()
print('PLAYER DIED')
