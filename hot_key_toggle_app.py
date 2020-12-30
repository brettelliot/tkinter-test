import tkinter as tk
import pynput
from AppKit import NSWorkspace

# The root needs to be created first, then the hot key listener, then the app. No idea why.
global_root = tk.Tk()


class HotKeyToggleApp:

    def __init__(self, root):

        # Setup the global hot key listener first.
        self.stop_listener = False
        self.hotkeys = pynput.keyboard.GlobalHotKeys({
            '<cmd>+<shift>': self.on_hot_key_press})
        self.hotkeys.start()
        self.my_name = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']

        # Then create the app
        self.root = root
        self.root.title("Hot key toggle app")

        # Set the window on top
        self.root.app_on_top = True
        self.root.attributes('-topmost', self.root.app_on_top)
        self.root.update()

        # Set the main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both", side="top")

        self.create_widgets(self.main_frame)

        # Handle quitting nicely
        self.root.protocol("WM_DELETE_WINDOW", self.safe_quit)

        # Kick off the main loop
        self.root.mainloop()

    def safe_quit(self):
        if not self.stop_listener:
            self.stop_listener = True
        self.hotkeys.stop()
        self.root.destroy()


    def on_hot_key_press(self):
        active_app = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
        if self.stop_listener:
            return False
        elif self.root.state() == 'withdrawn' or active_app != self.my_name:
            self.root.app_on_top = True
            self.root.lift()
            self.root.deiconify()
            self.root.focus_force()
            self.root.grab_set()
            self.root.grab_release()
            self.text.focus()
        else:
            self.root.withdraw()

        self.root.update()

    def create_widgets(self, main_frame):
        # Create the text box
        self.text = tk.Text(wrap="word", borderwidth=0, highlightthickness=0)
        self.text.pack(in_=main_frame, side="top", fill="both", expand=True)
        self.text.focus()


if __name__ == "__main__":
    app = HotKeyToggleApp(global_root)
