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

Todo:
* Hitting enter on a nested bullet should created an indented bullet
* Deal with clicking into an existing bulleted list and adding another bullet


"""
import tkinter as tk
from tkinter import font
import logging
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BulletedListText(tk.Text):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # tags
        self.bullet_char = '-'
        font_name = font.nametofont(self.cget("font"))
        # how much to indent the first line of a chunk of text
        lmargin1 = font_name.measure('mm')
        # how much to indent successive lines of a chunk of text
        lmargin2 = lmargin1 + font_name.measure(self.bullet_char)

        if logging.DEBUG >= logger.level:
            self.tag_configure('bullet_l0', lmargin1=lmargin1, background='red')
            self.tag_configure('bullet_l1', lmargin1=lmargin1, background='red')
            self.tag_configure('bullet_l2', lmargin1=lmargin1*2, background='red')
            self.tag_configure('bullet_text_l0', lmargin1=lmargin2, lmargin2=lmargin2, background='green')
            self.tag_configure('bullet_text_l1', lmargin1=lmargin2, lmargin2=lmargin2, background='green')
            self.tag_configure('bullet_text_l2', lmargin1=lmargin2*2, lmargin2=lmargin2*2, background='green')
        else:
            self.tag_configure('bullet_l0', lmargin1=lmargin1)
            self.tag_configure('bullet_l1', lmargin1=lmargin1)
            self.tag_configure('bullet_l2', lmargin1=lmargin1*2)
            self.tag_configure('bullet_text_l0', lmargin1=lmargin2)
            self.tag_configure('bullet_text_l1', lmargin1=lmargin2)
            self.tag_configure('bullet_text_l2', lmargin1=lmargin2*2)

        self.bullet_tag_levels = {
            0: 'bullet_l0',
            1: 'bullet_l1',
            2: 'bullet_l2'
        }

        self.bullet_text_tag_levels = {
            0: 'bullet_text_l0',
            1: 'bullet_text_l1',
            2: 'bullet_text_l2'
        }

        # events
        self.bullet_sym = ['minus', 'asterisk', 'plus']
        for b in self.bullet_sym:
            self.bind(f'<KeyPress-{b}>', self.apply_format)

        self.bind('<KeyPress-Return>', self.apply_format)
        self.bind('<KeyPress-Tab>', self.apply_format)

        # book keeping
        self.indentations = {}

    def apply_format(self, event: tk.Event):
        # current position - 1 (this is before insertion)
        position = self.index('insert')

        # convert line and character to int
        l = int(position.split('.')[0])
        c = int(position.split('.')[1])

        # Get all the tags for the current cursor position
        tags = self.tag_names(position)

        # Check if the user entered a bullet character at the start of a line
        if event.keysym in self.bullet_sym and c == 0:
            logger.debug(f'{position}: Creating first bullet of a bulleted list')
            # store the indentation level of the line
            self.indentations[l] = 1
            # add the bullet character at the beginning of the current line
            self.insert(f'{l}.0', f'{self.bullet_char}')
            # now add the bullet tag around the bullet char
            bullet_tag = self.bullet_tag_levels[self.indentations.get(l, 0)]
            self.tag_add(bullet_tag, f'{l}.0', f'{l}.1')
            # insert a space after the bullet char
            self.insert(f'{l}.1', ' ')
            # add the bullet_text tag around the text from the space to the end
            # of the line plus 1 character for the \n
            bullet_text_tag = self.bullet_text_tag_levels[self.indentations.get(l, 0)]
            self.tag_add(bullet_text_tag, f'{l}.1', f'{l}.end+1c')
            return 'break'

        # Check if the user hit return
        elif event.keysym == 'Return':
            # Check if the user hit return on a bulleted line
            # if 'bullet_text' in tags:
            if any('bullet_text' in s for s in tags):
                # If the user hit return on a bulleted line and the return was the hit just after a previous return
                # meaning the user hit return twice, then get out of bulleted list mode.
                if c == 2:
                    logger.debug(f'{position}: Ending bulleted list')
                    # Remove the bullet tag from the start of the line
                    bullet_tag = self.bullet_tag_levels[self.indentations.get(l, 0)]
                    self.tag_remove(bullet_tag, f'{l}.0', f'{l}.end')
                    # Remove the bullet_text tag from the start of the line
                    bullet_text_tag = self.bullet_text_tag_levels[self.indentations.get(l, 0)]
                    self.tag_remove(bullet_text_tag, f'{l}.0', f'{l}.end+1c')
                    # Delete any text on the line which would include the bullet and extra added space
                    self.delete(f'{l}.0', f'{l}.end')
                    # remove the indentation level of the line
                    self.indentations[l] = 0
                # Otherwise, just add a another bullet
                else:
                    logger.debug(f'{position}: Adding a bullet to a bulleted list')
                    # Remove any bullet_text tag from the entire next line before adding anything.
                    # The start of the next line is referenced by the first character of the next line minus one
                    # character and goes until the next line's end.
                    bullet_text_tag = self.bullet_text_tag_levels[self.indentations.get(l, 0)]
                    self.tag_remove(bullet_text_tag, f'{l + 1}.0-1c', f'{l + 1}.end')
                    # Then add the new line
                    self.insert(position, f'\n')
                    # store the indentation level of the line
                    self.indentations[l+1] = 1
                    # Then insert the bullet char
                    self.insert(f'{l+1}.0', f'{self.bullet_char}')
                    # Then insert the bullet tag
                    bullet_tag = self.bullet_tag_levels[self.indentations.get(l+1, 0)]
                    self.tag_add(bullet_tag, f'{l+1}.0', f'{l+1}.1')
                    # Then insert the space
                    self.insert(f'{l+1}.1', ' ')
                    # Finally add the bulleted text tag for the whole new line
                    bullet_text_tag = self.bullet_text_tag_levels[self.indentations.get(l+1, 0)]
                    self.tag_add(bullet_text_tag, f'{l+1}.1', f'{l+1}.end+1c')
            # If the user hit return when not in a bulleted line, just add a regular new line
            else:
                logger.debug(f'{position}: Adding a regular old new line.')
                self.insert(position, f'\n')

        # Check if the user hit tab
        elif event.keysym == 'Tab':
            # Check if the user hit tab on a bulleted line
            bullet_text_tag = self.bullet_text_tag_levels[self.indentations.get(l, 0)]
            if bullet_text_tag in tags:
                # If the user hit tab at the start of a new bulleted line then add a nested bullet
                if c == 2:
                    logger.debug(f'{position}: Adding nested bullet')
                    # Remove the bullet tag from the start of the line
                    bullet_tag = self.bullet_tag_levels[self.indentations.get(l, 0)]
                    self.tag_remove(bullet_tag, f'{l}.0', f'{l}.end+1c')
                    # Remove the bullet_text tag from the start of the line
                    bullet_text_tag = self.bullet_text_tag_levels[self.indentations.get(l, 0)]
                    self.tag_remove(bullet_text_tag, f'{l}.0', f'{l}.end+1c')
                    # Delete any text on the line which would include the bullet and extra added space
                    self.delete(f'{l}.0', f'{l}.end')
                    # store the indentation level of the line
                    self.indentations[l] += 1
                    # Then insert the bullet char
                    self.insert(f'{l}.0', f'{self.bullet_char}')
                    # Then insert the bullet tag
                    bullet_tag = self.bullet_tag_levels[self.indentations.get(l, 0)]
                    self.tag_add(bullet_tag, f'{l}.0', f'{l}.1')
                    # Then insert the space
                    self.insert(f'{l}.1', ' ')
                    # Finally add the bulleted text tag for the whole new line
                    bullet_text_tag = self.bullet_text_tag_levels[self.indentations.get(l, 0)]
                    self.tag_add(bullet_text_tag, f'{l}.1', f'{l}.end+1c')

        return 'break'
