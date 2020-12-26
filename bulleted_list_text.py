"""
The BulletedListText widget adds simple bulleted list functionality to the standard text widget.

Creating a bulleted list:
* When the first character in a new line one of the bullet characters (asterisk, minus, or plus) start a bulleted list.

Properties of a bulleted list:
* The bullet character is surrounded by a space on each side.
* The text on the bulleted line soft wraps and is indented to align with the first char in the bulleted line.

Exiting a bulleted list:
* Given the user is in the middle of making a bulleted list, when they hit return, and then return again,
first, a new line with new bullet is created, and then that is removed and the bulleted list ends,
and normal text is inserted afterwards.


"""
import tkinter as tk
from tkinter import font


class BulletedListText(tk.Text):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # tags
        self.bullet_char = '-'
        font_name = font.nametofont(self.cget("font"))
        lmargin1 = font_name.measure(self.bullet_char)
        lmargin2 = lmargin1 + font_name.measure(self.bullet_char + ' ')
        self.tag_configure("bullet", lmargin1=lmargin1)
        self.tag_configure("bullet_text", lmargin1=lmargin2, lmargin2=lmargin2)

        # events
        self.bullet_sym = ['minus', 'asterisk', 'plus']
        for b in self.bullet_sym:
            self.bind(f'<KeyPress-{b}>', self.apply_format)

        self.bind('<KeyPress-Return>', self.apply_format)

    def apply_format(self, event: tk.Event):
        # current position - 1 (this is before insertion)
        position = self.index('insert')

        # convert line and character to int
        l = int(position.split('.')[0])
        c = int(position.split('.')[1])

        # apply formatting accordingly
        if event.keysym in self.bullet_sym and c == 0:
            # print("Creating first bullet of a bulleted list")
            self.insert(f'{l}.0', f'{self.bullet_char}')
            self.tag_add('bullet', f'{l}.0', f'{l}.1')
            self.insert(f'{l}.1', ' ')
            self.tag_add('bullet_text', f'{l}.1', 'end+1c')
            return 'break'
        elif event.keysym == 'Return':
            tags = self.tag_names(position)
            if 'bullet_text' in tags:
                # print("Adding a bullet to a bulleted list")
                self.tag_remove("bullet_text", f'{l + 1}.0-1c', 'end')
                self.insert(position, f'\n')
                self.insert(f'{l+1}.0', f'{self.bullet_char}')
                self.tag_add('bullet', f'{l+1}.0', f'{l+1}.1')
                self.insert(f'{l+1}.1', ' ')
                self.tag_add('bullet_text', f'{l+1}.1', 'end+1c')
            else:
                # print("Ending bulleted list")
                self.insert(position, f'\n')
                self.tag_remove('bullet', f'{l + 1}.0-1c', 'end')
                self.tag_remove('bullet_text', f'{l + 1}.0-1c', 'end')

            self.see(self.index('insert+1l'))
            return 'break'
