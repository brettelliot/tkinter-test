import tkinter as tk
from tkinter import messagebox
from pynput import keyboard


def on_activate_hotkey():
    print('<cmd>+<shift> pressed')


root = tk.Tk()

hotkeys = keyboard.GlobalHotKeys({
    '<cmd>+<shift>': on_activate_hotkey})

hotkeys.start()
root.mainloop()
