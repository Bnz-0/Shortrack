# Shortrack

**Shortrack is a potentially fun script that permit to play track using keyboard-shortcut.**

Each shortcut is associated to a track and holding down all the keys the track starts playing as long as they are held down.
Every shortcuts and trucks are completely configurable, so you can use it with every kind of audio and combination of keys

## Installation
> On **Windows** you need to have [python](https://www.python.org/downloads/) installed  
> (maybe also the [visual c++ build tools](https://visualstudio.microsoft.com/it/visual-cpp-build-tools/?rr=https%3A%2F%2Fgithub.com%2Fbenfred%2Fimplicit%2Fissues%2F76))

1. `$ git clone git@github.com:Bnz-0/Shortrack.git && cd Shortrack`
2. `$ pip install -r requirements.txt`
3. `$ python3 shortrack.py`
4. **Raise up the volume** and keep pressed "`alt+shift+p`" to launch a _safe_ audio test ;)
5. To quit press "`alt+0`" (unless you've already modified the QUIT shortcut in `hotkeys.conf` file)

> If something goes wrong, go to [Issues](#Issues)

## Configuration
All you need to do is modify the file "`hotkeys.conf`".  
The syntax is really simple, each line define a **shortrack** in this way:

`<keys>:<rel_path>`

Where `keys` are the keys you choose to press to trigger the track and `rel_path` is the **relative** path to a .wav file

> The keys must be written like [this specification](https://github.com/boppreh/keyboard#keyboardparse_hotkeyhotkey).  
> Simply: **keys separated by a _+_**

There are also a special keyword which you can use as a path:
- **QUIT**: the hotkey associated to this will kill the script's execution

> You can take a look at the standard `hotkeys.conf` in this repo for a simple example

## Notes:
- All file audio must be a `wav` file
- The `hotkeys.conf` must be placed in the same directory of the script
- The path to the tracka is relative to the script folder

## Issues
First of all, check if you are running the script using **python3**. I don't know if it works also with python2 but please, stop to use it and accept his death

> If something goes bad, you can find all error raised in the file `shortrack.log` (in the same folder of shortrack.py)

- If the installation fails, try to install the dependencies of PyAudio: https://people.csail.mit.edu/hubert/pyaudio/

- On Windows the _pyaudio_ package have some installation problems, if `pip` doesn't work you can find the same package for windows [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).  
    So just download it and install it doing `$ pip install .\PyAudio‑<version you have downloaded>.whl`

- If you're trying to run it on macOS, probably it doesn't work because of packages. If you want to make it works also on macOS fell free to fix this and make a pull request!

---

### What the hell is the "simpler solution"?
Well, it's the first solution I've made, but in linux it have a big problem:

Because of `keyboard` package (that allow the script to listen every keyboard you press) in Linux you have to run this as **root user**, but for some reason when it try to play an audio it often found the device _busy_ and raise this error:

`ALSA lib pcm_dmix.c:1089:(snd_pcm_dmix_open) unable to open slave`

That's why in the actual version there's 2 different process: the **listener** and the **player**, running as different users.

**"Why you keep both version?"**\
Because the first one is shorter, simplier, all in a single file, runs as a single process, **it doesn't open any kind socket** and finally... **it works on Windows** (yeah, every kind of process can listen the keyboard without a particular permission... good luck Windows users!)

So basically is a nicer solution with some problems and I decided to keep it here just in case

