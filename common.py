import sys, platform, os, threading, socket
from time import gmtime, strftime, sleep

SLASH = '\\' if platform.system()=="Windows" else '/'
PATH = sys.argv[0][:sys.argv[0].rfind(SLASH)+1] if SLASH in sys.argv[0] else "."+SLASH

ACK_SGN = b'\xfe' # the other process is ready
STP_SGN = b'\xff' # the hotkey was released

def read_hk():
	"Read the hotkeys.conf file and returns a list of tuple `(hotkey, path|QUIT)`"
	with open(PATH+"hotkeys.conf", 'r') as f:
		hks = [tuple(l.split(':')) for l in f.read().splitlines()]
	if len(hks) >= STP_SGN[0]:
		raise Exception(f"Read {len(hks)} hotkeys, but the max length allowed is {STP_SGN[0]-1}")
	return hks

def log(msg):
	s = f"{strftime('%Y-%m-%d %H:%M:%S', gmtime())}: {msg}\n"
	print('LOG', s)
	with open(PATH+'shortrack.log', 'a+') as f:
		f.write(s)
