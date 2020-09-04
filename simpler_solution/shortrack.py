#!/bin/env python3
import keyboard as kb
import pyaudio, wave, threading, sys, platform
from time import sleep, gmtime, strftime


SLASH = '\\' if platform.system()=="Windows" else '/'
PATH = sys.argv[0][:sys.argv[0].rfind(SLASH)+1] if SLASH in sys.argv[0] else ""
CHUNK = 1024
quit_event = threading.Event()
lock = threading.Lock()
p = None


def log(msg):
    s = f"{strftime('%Y-%m-%d %H:%M:%S', gmtime())}: {msg}\n"
    print('LOG', s)
    with open(PATH+'shortruck.log', 'a+') as f:
        f.write(s)


def play(src, hotkey):
    lock.acquire()
    try:
        with wave.open(src, 'rb') as wf:
            data = None
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            while data != b'' and kb.is_pressed(hotkey):
                data = wf.readframes(CHUNK)
                stream.write(data)

            stream.stop_stream()
            stream.close()

    except Exception as e:
        log(f"play({src}, {hotkey}) -> {str(e)}")
        reset()
    finally:
        lock.release()


def reset():
    global p
    p.terminate()
    p = pyaudio.PyAudio()


def end_of_the_fun():
    quit_event.set()


try:
    with open(PATH+"hotkeys.conf", 'r') as f:
        for conf in f.read().splitlines():
            hotkey, src = conf.split(':')
            if src == 'QUIT':
                kb.add_hotkey(hotkey, end_of_the_fun)
            elif src == 'RESET':
                kb.add_hotkey(hotkey, reset)
            else:
                kb.add_hotkey(hotkey, play, args=[PATH+src, hotkey])

except Exception as e:
    log(f"Error while reading \"{PATH}hotkeys.conf\": {str(e)}")

else:
    p = pyaudio.PyAudio()
    try:
        quit_event.wait()
    except Exception as e:
        log(f"Error while waiting: {str(e)}")
    finally:
        p.terminate()
