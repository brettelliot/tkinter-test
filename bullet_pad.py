from hot_key_toggle_app import HotKeyToggleApp
from hot_key_toggle_app import global_root
from bulleted_list_text import BulletedListText


class BulletPadApp(HotKeyToggleApp):

    def __init__(self, root):
        super().__init__(root)

    def create_widgets(self, main_frame):
        # Create the text box
        self.root.title("Bullet Pad")
        self.text = BulletedListText(wrap="word", borderwidth=0, highlightthickness=0)
        self.text.pack(in_=self.main_frame, side="top", fill="both", expand=True)
        self.text.focus()


if __name__ == "__main__":
    app = BulletPadApp(global_root)
