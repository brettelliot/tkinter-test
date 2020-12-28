import tkinter as tk
from tkinter import font as font
"""
This shows the problem.

I'm building a bulleted list text widget with python and tkinter. I'd like the bullets themselves to be "non-editable", meaning the user can't delete the actual bullet character. I've created a simple example to show the problem. In my example I add a bullet ("-") and then two spaces. The user can backspace and delete the bullet and the two spaces I added, but I don't want them to be able to. I want them to be able to backspace only up to the "B" in "Bullet example".

I thought that by using two tags, one for the bullet, and one for the text on the bulleted line, i'd be able to do that. It sort of works. The bullet tag adds a left margin that the user can't delete past, but the bullet character and the spaces i'm using for padding are unfortunately still deletable.

How can I create a non-deletable bullet (with a margin on its left and right) within a text widget that is editable by the user?

"""


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
