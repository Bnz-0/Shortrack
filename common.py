import sys, platform, os, threading, socket, re
from time import gmtime, strftime, sleep

SLASH = '\\' if platform.system()=="Windows" else '/'
PATH = sys.argv[0][:sys.argv[0].rfind(SLASH)+1] if SLASH in sys.argv[0] else "."+SLASH

ACK_SGN = b'\xfe' # the other process is ready
STP_SGN = b'\xff' # the hotkey was released

def read_hk():
	"Read the hotkeys.conf file and returns a list of tuple `(mod, hotkey, path|QUIT)`"
	with open(PATH+"hotkeys.conf", 'r') as f:
		hks = []
		for l in f.read().splitlines():
			l = l.strip()
			if len(l) == 0 or l[0] == '#': continue
			t = tuple(l.split(':'))
			assert 2 <= len(t) <= 3, "Malformed line in hotkeys.conf: " + l
			if len(t) == 2: t = ('', *t)
			hks.append(t)
	if len(hks) >= STP_SGN[0]:
		raise Exception(f"Read {len(hks)} hotkeys, but the max length allowed is {STP_SGN[0]-1}")
	return hks

def log(msg):
	s = f"{strftime('%Y-%m-%d %H:%M:%S', gmtime())}: {msg}\n"
	print('LOG', s, file=sys.stderr)
	with open(PATH+'shortrack.log', 'a+') as f:
		f.write(s)
	if platform.system() != "Windows" and os.getuid() == 0:
		os.chmod(PATH+'shortrack.log', 0o666) # sets permissions in case the unprivileged process have to log something
