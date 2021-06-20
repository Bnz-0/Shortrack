#!/bin/env python3
import sys, os, threading, platform, socket
import pyaudio, wave
from common import PATH, read_hk, log, pjoin, \
	ACK_SGN, STP_SGN, \
	QUIT, RESUME, PAUSE, PAUSE_RESUME


class State:
	def __init__(self, mode = 'd', hotkey = None, src = None, is_playing = False, active = True):
		self.hotkey = hotkey
		self.src = src
		self.mode = mode
		self.is_playing = is_playing
		self.active = active

	def update(self, other_state):
		self.mode = other_state.mode
		self.hotkey = other_state.hotkey
		self.src = other_state.src

	def __str__(self):
		return f'hotkey="{self.hotkey}" src="{self.src}" mode={self.mode} is_playing={self.is_playing}'


class Player:
	def __init__(self, state, p):
		self._player = None
		self.state = state
		self.pyaudio = p

	def start(self):
		self._player = threading.Thread(target=self._play)
		self._player.start()

	def stop(self):
		self.state.is_playing = False
		if self._player is not None:
			self._player.join()
			self._player = None

	def _play(self):
		self.state.is_playing = True
		try:
			while True:
				with wave.open(pjoin(PATH, self.state.src), 'rb') as wf:
					data = None
					stream = self.pyaudio.open(
						format=self.pyaudio.get_format_from_width(wf.getsampwidth()),
						channels=wf.getnchannels(),
						rate=wf.getframerate(),
						output=True
					)
					while self.state.is_playing and data != b'':
						data = wf.readframes(1024)
						stream.write(data)
					stream.stop_stream()
					stream.close()
					if not self.state.is_playing or 'l' not in self.state.mode:
						break
		except Exception as e:
			log(f"play() [{self.state}] -> {str(e)}")
		finally:
			self.state.is_playing = False


def spawn_listener(soc):
	spawn_foo, path = (os.spawnlp, pjoin(PATH, 'hk_listener.py')) \
		if platform.system() != "Windows" else \
		(os.spawnl, '"'+pjoin(PATH, 'hk_listener.py"'))

	spawn_foo(
		os.P_NOWAIT,
		sys.executable,
		sys.executable,
		path,
		str(soc.getsockname()[1])
	)


def play_loop(state, player, recv):
	hklist = read_hk()
	while True:
		try:
			index = recv()
			new_state = None

			if index == STP_SGN[0]:
				new_state = State()
			elif index < len(hklist):
				new_state = State(*hklist[index], False)
			else:
				log(f"Invalid index recieved: {index}")
				continue

			if new_state.src == QUIT:
				player.stop()
				break
			if new_state.src == PAUSE:
				player.stop()
				state.active = False
				continue
			if new_state.src == RESUME:
				state.active = True
				continue
			if new_state.src == PAUSE_RESUME:
				player.stop()
				state.active = not state.active
				continue

			if not state.active: continue

			if 'c' in state.mode:
				if new_state.hotkey is None: continue
				if state.is_playing and new_state.hotkey == state.hotkey:
					player.stop()
					state = player.state = State()
					continue

			if state.is_playing and new_state.hotkey != state.hotkey:
				player.stop()
			state.update(new_state)
			if state.hotkey is not None:
				player.start()

		except Exception as e:
				log(f"listening for hotkeys -> {str(e)}")


def wait_for_listener(soc):
	listener_addr = None
	ack = None
	try: # wait for the listener
		while ack != ACK_SGN:
			ack, listener_addr = soc.recvfrom(1)
			soc.sendto(ACK_SGN, listener_addr)
	except Exception as e:
			log(f"waiting for the listener (recv={ack}, addr={listener_addr}) -> {str(e)}")
			sys.exit(1)
	return listener_addr


def main():
	soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	soc.bind(('127.0.0.1', 0))
	spawn_listener(soc)

	listener_addr = wait_for_listener(soc)

	state = State()
	p = pyaudio.PyAudio()
	def recv():
		(index,*_), addr = soc.recvfrom(1)
		print('PLAYER recv', index, addr)
		if addr != listener_addr:
			raise PermissionError(f"recv from {addr}, expected {listener_addr}")
		return index

	print('PLAYER READY')
	play_loop(state, Player(state, p), recv)
	p.terminate()
	soc.close()
	print('PLAYER DIED')


if __name__ == '__main__':
	main()
