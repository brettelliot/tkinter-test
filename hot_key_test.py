from pynput import keyboard


def on_activate_hotkey():
    print('hotkey pressed')


with keyboard.GlobalHotKeys({
    '<cmd>+<shift>': on_activate_hotkey,
    '<ctrl>+<shift>': on_activate_hotkey
}) as h:
    h.join()
