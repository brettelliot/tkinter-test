# This tests adding an embedded widget to a text widget.

import tkinter as tk
from tkinter import font as tkFont


class EmbeddedBulletText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_font = tkFont.nametofont(self.cget("font"))

        em = default_font.measure("m")
        default_size = default_font.cget("size")
        bold_font = tkFont.Font(**default_font.configure())
        italic_font = tkFont.Font(**default_font.configure())
        h1_font = tkFont.Font(**default_font.configure())

        bold_font.configure(weight="bold")
        italic_font.configure(slant="italic")
        h1_font.configure(size=int(default_size * 2), weight="bold")

        self.tag_configure("bold", font=bold_font)
        self.tag_configure("italic", font=italic_font)
        self.tag_configure("h1", font=h1_font, spacing3=default_size)

        self.bullet_str_var = tk.StringVar()
        self.bullet_str_var.set(f'  \u2022  ')

        lmargin2 = em + default_font.measure(self.bullet_str_var)
        self.tag_configure("bullet", lmargin1=em, lmargin2=lmargin2)

    def insert_bullet(self, index, text):
        label = tk.Label(self, textvariable=self.bullet_str_var)
        self.window_create('end', window=label)
        self.insert(index, f'{text}', 'bullet')


if __name__ == "__main__":

    root = tk.Tk()

    text = EmbeddedBulletText(root, width=40, height=15)
    text.insert("end", "Rich Text Example\n", "h1")

    text.pack(fill="both", expand=True)

    text.insert("end", "Hello, world\n\n")
    text.insert_bullet("end", "Item 1\n")
    text.insert_bullet("end", "Item 2\n")

    text.insert("end", "\n")
    text.insert("end", "This line is bold\n", "bold")
    text.insert("end", "This line is italicized\n", "italic")

    root.mainloop()
