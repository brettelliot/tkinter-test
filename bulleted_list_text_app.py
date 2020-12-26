import tkinter as tk
from bulleted_list_text import BulletedListText

global_root = tk.Tk()


class MyApp:

    def __init__(self, root):
        # Create the app
        self.root = root
        self.root.title("Bulleted list text test")

        # Set the main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both", side="top")

        # Create the text box
        self.text = BulletedListText(wrap="word", borderwidth=0, highlightthickness=0)
        self.text.pack(in_=self.main_frame, side="top", fill="both", expand=True)
        self.text.focus()

        # Kick off the main loop
        self.root.mainloop()


if __name__ == "__main__":
    app = MyApp(global_root)
