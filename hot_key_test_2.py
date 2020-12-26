import tkinter as tk
from tkinter import messagebox
from pynput import keyboard

def call_me(event=""):
    messagebox.showinfo("trying","thisa")


root = tk.Tk()


button = tk.Button(root, text="call me", command = call_me)


button.pack()

root.geometry("300x300")

hotkeys = keyboard.GlobalHotKeys({
    '<cmd>+<shift>': call_me})

hotkeys.start()
root.mainloop()
