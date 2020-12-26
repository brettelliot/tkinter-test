import tkinter as tk
from tkinter import font as tkFont
from pynput import keyboard


'''
Bulleted list requirements
* Bullet list editing is kind of like a mode. If your cursor is in a bulleted list, then you're in the mode.
* Enabling bulleted list mode takes the line, indents it, and adds a bullet.
* You can get into bulleted list mode by starting a new line and typing a hyphen and then a space
 (or an asterik and then a space). It then auto indents. However if you type hypen space then backspace it kicks you
 out of bulleted list mode and just inserts a hypen and a space. (This is google docs behavior. 
 Alternatively, MS word gets out of bulleted list mode by making you type cmd-z) 
'''


class App(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        # Set the window on top
        self.app_on_top = True
        self.attributes('-topmost', self.app_on_top)
        self.update()

        ## Toolbar
        self.toolbar = tk.Frame()

        self.bullet = tk.Button(name="toolbar", text="bullet",
                                borderwidth=1, command=self.on_bullet,)
        self.bullet.pack(in_=self.toolbar, side="left")

        ## Main part of the GUI
        # I'll use a frame to contain the widget and
        # scrollbar; it looks a little nicer that way...
        text_frame = tk.Frame(borderwidth=1, relief="sunken")
        self.text = tk.Text(wrap="word", borderwidth=0, highlightthickness=0)
        self.vsb = tk.Scrollbar(orient="vertical", borderwidth=1, command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(in_=text_frame,side="right", fill="y", expand=False)
        self.text.pack(in_=text_frame, side="left", fill="both", expand=True)
        self.toolbar.pack(side="top", fill="x")
        text_frame.pack(side="bottom", fill="both", expand=True)

        # self.text.bind('<Return>', self.autoindent2)

        # self.text.bind('<Control-Key-n>', self.toggle_app_window)

    #
    # def on_activate_hotkey(self):
    #     print('<cmd>+<shift> pressed')

    def toggle_app_window():
        print("were in!")

    def toggle_app_window2(self):
        self.app_on_top = not self.app_on_top
        print("app_on_top = {}", self.app_on_top)
        self.attributes('-topmost', self.app_on_top)
        if self.app_on_top:
            self.lift()
        else:
            self.lower()
        self.update()

    def on_bullet(self):
        self.text.insert("end", f"\u2022 ", "bullet")

    def autoindent2(self, event):
        """
            this method implements the callback for the Return Key in the editor widget.
            arguments: the tkinter event object with which the callback is associated
        """
        indentation = ""
        lineindex = self.text.index("insert").split(".")[0]
        linetext = self.text.get(lineindex+".0", lineindex+".end")

        for character in linetext:
            if character in [" ","\t"]:
                indentation += character
            else:
                break

        self.text.insert(self.text.index("insert"), "\n"+indentation)
        return "break"

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


if __name__ == "__main__":
    app=App()

    listener = keyboard.GlobalHotKeys({'<cmd>+<shift>': app.toggle_app_window})
    listener.start()
    app.mainloop()

    # listener.stop()
    # listener.join()