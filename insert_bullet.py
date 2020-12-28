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

    def insert_bullet(self, position, text):
        # convert line and character to int
        line = int(position.split('.')[0])
        col = int(position.split('.')[1])

        self.insert(f'{line}.0', self.bullet_char)
        self.tag_add('bullet',f'{line}.0',f'{line}.1')
        self.insert(f'{line}.1', f'{self.num_spaces_after_bullet*" "}')
        self.tag_add('bullet_text', f'{line}.1', f'{line}.end+1c')
        self.insert(f'{line}.3', text)


if __name__ == "__main__":
    root = tk.Tk()
    text = BulletText(root, width=40, height=15)
    text.pack(fill="both", expand=True)

    position = text.index('insert')
    text.insert_bullet(position, "Bullet example")

    root.mainloop()
