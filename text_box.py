import tkinter as tk

window = tk.Tk()
frame = tk.Frame(master=window)
frame.pack(fill=tk.BOTH, expand=True)
txt_box = tk.Text(master=frame)
txt_box.pack(fill=tk.BOTH, expand=True)
window.mainloop()