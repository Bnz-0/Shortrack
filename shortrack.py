#!/bin/env python3
from common import *
import pyaudio, wave

class State:
	def __init__(self, mode = 'd', hotkey = None, src = None, is_playing = False, active = True):
		self.hotkey = hotkey
		self.src = src
		self.mode = mode
		self.is_playing = is_playing
		self.active = active

	def __str__(self):
		return f'hotkey="{self.hotkey}" src="{self.src}" mode={self.mode} is_playing={self.is_playing}'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1',0))

# spawn the listener
if platform.system() != "Windows":
	os.spawnlp(os.P_NOWAIT,
		sys.executable, sys.executable,
		os.path.dirname(os.path.abspath(__file__))+SLASH+'hk_listener.py', str(s.getsockname()[1])
	)
else:
	os.spawnl(os.P_NOWAIT,
		sys.executable, sys.executable,
		'"'+os.path.dirname(os.path.abspath(__file__))+SLASH+'hk_listener.py"', str(s.getsockname()[1])
	)

HKLIST = read_hk()
state = State()
p = pyaudio.PyAudio()
listener_addr = None
r = player = None

def play():
	global state
	state.is_playing = True
	try:
		while True:
			with wave.open(PATH+state.src, 'rb') as wf:
				data = None
				stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
								channels=wf.getnchannels(),
								rate=wf.getframerate(),
								output=True)
				while state.is_playing and data != b'':
					data = wf.readframes(1024)
					stream.write(data)
				stream.stop_stream()
				stream.close()
				if not state.is_playing or 'l' not in state.mode:
					break
	except Exception as e:
		log(f"play() [{state}] -> {str(e)}")
	finally:
		state.is_playing = False

def start_play():
	global player
	player = threading.Thread(target=play)
	player.start()

def stop_play():
	global player
	state.is_playing = False # trigger the player to stop
	if player is not None:
		player.join()
		player = None


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


while True:
	try:
		(index,*_), addr = s.recvfrom(1)
		print('PLAYER recv', index, addr)
		if addr != listener_addr: continue

		new_state = None
		if index == STP_SGN[0]:
			new_state = State()
		elif index < len(HKLIST):
			new_state = State(*HKLIST[index], False)
		else: # invalid index
			log(f"Invalid index recieved: {index}")
			continue

		if new_state.src == 'QUIT':
			stop_play()
			break
		if new_state.src == 'PAUSE':
			stop_play()
			state.active = False
			continue
		if new_state.src == 'RESUME':
			state.active = True
			continue
		if new_state.src == 'PAUSE_RESUME':
			stop_play()
			state.active = not state.active
			continue

		if not state.active: continue

		if 'c' in state.mode:
			if new_state.hotkey is None: continue
			if state.is_playing and new_state.hotkey == state.hotkey:
				stop_play()
				state = State()
				continue

		if state.is_playing and new_state.hotkey != state.hotkey:
			stop_play()
		state.mode, state.hotkey, state.src = new_state.mode, new_state.hotkey, new_state.src
		if state.hotkey is not None:
			start_play()

	except Exception as e:
			log(f"listening for hotkeys (recv={r}, addr={addr}, listener_addr={listener_addr}) -> {str(e)}")

p.terminate()
s.close()
print('PLAYER DIED')

