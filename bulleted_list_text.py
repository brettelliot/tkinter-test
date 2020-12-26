"""
The BulletedListText widget adds simple bulleted list functionality to the standard text widget.

Creating a bulleted list:
* When the first character in a new line one of the bullet characters (asterisk, minus, or plus) start a bulleted list.

Properties of a bulleted list:
* The bullet character is surrounded by a space on each side.  
Bulleted list requirements
* Bullet list editing is kind of like a mode. If your cursor is in a bulleted list, then you're in the mode.
* Enabling bulleted list mode takes the line, indents it, and adds a bullet.
* You can get into bulleted list mode by starting a new line and typing a hyphen and then a space
 (or an asterik and then a space). It then auto indents. However if you type hypen space then backspace it kicks you
 out of bulleted list mode and just inserts a hypen and a space. (This is google docs behavior.
 Alternatively, MS word gets out of bulleted list mode by making you type cmd-z)

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
