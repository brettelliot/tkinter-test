from tkinter import *
root = Tk()

def f(event):
    print(event.x, event.y)

# root.bind("<Motion>", f)
print(f'{root.winfo_screen(), root.winfo_}')
root.mainloop()