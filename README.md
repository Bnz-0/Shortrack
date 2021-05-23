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

`[mode:]<keys>:<rel_path>`

Where `keys` are the keys you choose to press to trigger the track and `rel_path` is the **relative** path to a .wav file

> The keys must be written like [this specification](https://github.com/boppreh/keyboard#keyboardparse_hotkeyhotkey).
> Simply: **keys separated by a _+_**

### Modes
The `mode` is an optional parameter that specifies the behavior of the track:
- _default_: the track is reproduced only when all the `keys` is held down
- **c** (continues): when all the `keys` are pressed the track starts playing and it will stops only after the same `keys` are pressed again
- **l** (loop): when the track finishes it restart from the beginning

> The modes can be put in combo, for example 'cl' create a track that go without keeping the keys hold down and restart when it finishes.

### Special keys
There are also special keywords which you can use as a `rel_path`:
- **QUIT**: the hotkey associated to this will kill the script's execution
- **PAUSE**: this will ignore any track to be played until RESUME
- **RESUME**: resume the standard behavior (i.e. plays again the tracks)
- **PAUSE_RESUME**: if you need to have both PAUSE and RESUME in the same hotkey, simply switches between PAUSE and RESUME each time the hotkey is pressed

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

