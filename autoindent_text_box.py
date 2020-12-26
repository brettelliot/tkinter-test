#
# from here:
# https://www.mmbyte.com/article/9717.html
#
import tkinter as tk
import re

root = tk.Tk()
text = tk.Text(root)
text.pack(fill="both", expand=True)


def autoindent(event):
    # the text widget that received the event
    widget = event.widget

    # get current line
    line = widget.get("insert linestart", "insert lineend")

    # compute the indentation of the current line
    match = re.match(r'^(\s+)', line)
    current_indent = len(match.group(0)) if match else 0

    # compute the new indentation
    new_indent = current_indent + 4

    # insert the character that triggered the event,
    # a newline, and then new indentation
    widget.insert("insert", event.char + "\n" + " "*new_indent)

    # return 'break' to prevent the default behavior
    return "break"

text.bind(":", autoindent)

root.mainloop()