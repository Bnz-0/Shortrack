import sys, platform, os
from time import gmtime, strftime

PATH = os.path.dirname(__file__) or '.'

# special keys
QUIT = 'QUIT'
PAUSE = 'PAUSE'
RESUME = 'RESUME'
PAUSE_RESUME = 'PAUSE_RESUME'

ACK_SGN = b'\xfe' # the other process is ready
STP_SGN = b'\xff' # the hotkey was released

pjoin = os.path.join

def read_hk():
	"Read the hotkeys.conf file and returns a list of tuple `(mod, hotkey, path|QUIT)`"
	with open(pjoin(PATH,"hotkeys.conf"), 'r') as f:
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
	with open(pjoin(PATH,'shortrack.log'), 'a+') as f:
		f.write(s)
	if platform.system() != "Windows" and os.getuid() == 0:
		os.chmod(pjoin(PATH,'shortrack.log'), 0o666) # sets permissions in case the unprivileged process has to log something
