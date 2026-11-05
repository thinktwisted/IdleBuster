# IdleBuster

A small Python script that keeps a Windows PC from going idle. It watches the
system idle timer and, just before the threshold is crossed, presses **Shift**
to reset it — so the screen doesn't sleep, the workstation doesn't lock, and
apps like Microsoft Teams or Slack keep showing you as *Active*.

## How it works

1. Prompts for your idle timeout in minutes.
2. Polls the real system idle time every second
   (`win32api.GetTickCount() - win32api.GetLastInputInfo()`).
3. When idle time reaches the threshold, it presses **Shift** twice (Win32
   `keybd_event` via `ctypes`) and keeps polling; the idle timer never crosses
   the configured timeout.
4. On `Ctrl+C` it prints how many idle periods were prevented and exits.

## Requirements

- Windows (uses Win32 APIs; will not run on macOS/Linux)
- Python 3
- [`pywin32`](https://pypi.org/project/pywin32/) only — key injection uses
  stdlib `ctypes`, no other dependencies

## Install

```bat
pip install pywin32
git clone https://github.com/thinktwisted/IdleBuster
cd IdleBuster
```

## Usage

```bat
python IdleBuster.py
What is your idle time [1-60 minutes]? 7
7 is out of range, enter 1-60
What is your idle time [1-60 minutes]? 5
Idle time [sec]: 300
1 - Shift pressed idle time was 298.53
2 - Shift pressed idle time was 299.01
...
```

Set the value to match your actual Windows lock/sleep timeout
(*Settings → System → Power & battery → Screen and sleep*). If you enter more
than the real timeout, Windows will still lock/sleep first.

Stop with `Ctrl+C` at any point, including the prompt. The script only runs
while that window is open — closing it stops IdleBuster.

## Limitations

- **Windows only.**
- The synthesized Shift goes to whichever window is focused. Standalone Shift
  is harmless in practice, but it is still injected input.
- Once the workstation is locked (`Win+L`), key injection fails and the script
  can no longer prevent anything — it keeps trying regardless.
- No installer, no tray icon, no autostart; run it from a console.

## Notes

- The native Windows way to keep the display awake is
  `SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)`.
  It injects no input, but apps that watch for *real* user input (Teams "Away"
  status) will still flip to away — the keystroke approach here does not have
  that problem.
- Wakes fire at fixed one-second sampling intervals, so detection lands within
  ~1 s of the threshold no matter how long the configured timeout is; sleep
  overshoot does not accumulate across cycles.

## License

GPL-3.0 — see [LICENSE](LICENSE).
