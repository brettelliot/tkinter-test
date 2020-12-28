import tkinter as tk
from tkinter import font as font

class BulletText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bullet_char = '-'
        self.num_spaces_per_indent = 4
        self.num_spaces_after_bullet = 2
        font_name = font.nametofont(self.cget("font"))
        self.indent_width = font_name.measure(self.num_spaces_per_indent * ' ')
        self.bullet_width = font_name.measure(f'{self.bullet_char}{self.num_spaces_after_bullet * " "}')

        self.tag_configure('bullet', lmargin1=self.indent_width, background='red')
        self.tag_configure('bullet_text', lmargin1=self.indent_width, lmargin2=self.indent_width + self.bullet_width,
                           background='green')

        self.bind('<KeyPress-BackSpace>', self.on_backspace)
        self.bind('<KeyPress-Delete>', self.on_backspace)

    def insert_bullet(self, position, text):
        # convert line and character to int
        line = int(position.split('.')[0])
        col = int(position.split('.')[1])

        self.insert(f'{line}.0', self.bullet_char)
        self.insert(f'{line}.1', f'{self.num_spaces_after_bullet * " "}')
        self.tag_add('bullet', f'{line}.0', f'{line}.3')
        self.insert(f'{line}.3', text)
        self.tag_add('bullet_text', f'{line}.3', f'{line}.end+1c')


    def on_backspace(self, event):
        # current position - 1 (this is before insertion)
        position = self.index('insert')

        # convert line and character to int
        line = int(position.split('.')[0])
        col = int(position.split('.')[1])

        # Get all the tags for the current cursor position
        tags = self.tag_names(position)
        if any("bullet" in s for s in tags):
            if col in [0,1,2,3]:
                return 'break'


if __name__ == "__main__":
    root = tk.Tk()
    text = BulletText(root, width=40, height=15)
    text.pack(fill="both", expand=True)

    position = text.index('insert')
    text.insert_bullet(position, "Bullet example")

    root.mainloop()
