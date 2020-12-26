from pynput import keyboard

def on_activate_hotkey():
    print('<cmd>+<shift> pressed')

with keyboard.GlobalHotKeys({
    '<cmd>+<shift>': on_activate_hotkey}) as h:
    h.join()

