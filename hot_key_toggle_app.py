import tkinter as tk
import pynput

# The root needs to be created first, then the hot key listener, then the app. No idea why.
global_root = tk.Tk()


class HotKeyToggleApp:

    def __init__(self, root):

        # Setup the global hot key listener first.
        self.stop_listener = False
        self.hotkeys = pynput.keyboard.GlobalHotKeys({
            '<cmd>+<shift>': self.on_hot_key_press})
        self.hotkeys.start()

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
        self.root.destroy()

    def on_hot_key_press(self):
        if self.stop_listener:
            return False
        else:
            self.root.app_on_top = not self.root.app_on_top
            # print("app_on_top = {}", self.root.app_on_top)
            if self.root.app_on_top:
                self.root.lift()
                self.root.deiconify()
                self.root.focus_force()
                self.root.grab_set()
                self.root.grab_release()
                self.text.focus()
            else:
                self.root.withdraw()
            self.root.update()
            # print(self.root.winfo_screen())

    def create_widgets(self, main_frame):
        # Create the text box
        self.text = tk.Text(wrap="word", borderwidth=0, highlightthickness=0)
        self.text.pack(in_=main_frame, side="top", fill="both", expand=True)
        self.text.focus()


if __name__ == "__main__":
    app = HotKeyToggleApp(global_root)
