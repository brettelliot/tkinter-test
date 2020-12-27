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
* Hitting enter on a indented bullet should create another indented bullet (with infinite levels)
* Deal with clicking into an existing bulleted list and adding another bullet

  - 2
  - 2 aslkfjklasdjf lksj
      fkaslfjaskl;fjlkasfjlk
    - 4
      - 6
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
        # how much to indent the first line of a chunk of text, equal to two spaces
        self.indent_width = font_name.measure('  ')
        # how much to indent successive lines of a chunk of text, equal to the width of the bullet char and 1 space
        self.bullet_width = font_name.measure(f'{self.bullet_char} ')

        # events
        self.bullet_sym = ['minus', 'asterisk', 'plus']
        for b in self.bullet_sym:
            self.bind(f'<KeyPress-{b}>', self.apply_format)
        self.bind('<KeyPress-Return>', self.apply_format)
        self.bind('<KeyPress-Tab>', self.apply_format)

        # book keeping
        self.indentations = {}
        self.bullet_tag_levels = {}
        self.bullet_text_tag_levels = {}

    def ilevel(self, level):
        return self.indentations.get(level, 0)

    def set_ilevel(self, level, value):
        self.indentations[level] = value

    def bullet_tag(self, level):
        if level in self.bullet_tag_levels:
            return self.bullet_tag_levels[level]
        else:
            bullet_tag = f'bullet_l{level}'
            if logging.DEBUG >= logger.level:
                self.tag_configure(
                    bullet_tag,
                    lmargin1=self.indent_width + (self.indent_width*level),
                    background='red')
            else:
                self.tag_configure(
                    bullet_tag,
                    lmargin1=self.indent_width + (self.indent_width*level))
            self.bullet_tag_levels[level] = bullet_tag
            return bullet_tag

    def bullet_text_tag(self, level):
        if level in self.bullet_text_tag_levels:
            return self.bullet_text_tag_levels[level]
        else:
            bullet_text_tag = f'bullet_text_l{level}'
            if logging.DEBUG >= logger.level:
                self.tag_configure(
                    bullet_text_tag,
                    lmargin1=self.indent_width + (self.indent_width*level),
                    lmargin2=(self.indent_width + (self.indent_width*level))+self.bullet_width,
                    background='green')
            else:
                self.tag_configure(
                    bullet_text_tag,
                    lmargin1=self.indent_width + (self.indent_width*level),
                    lmargin2=(self.indent_width + (self.indent_width*level))+self.bullet_width)
            self.bullet_text_tag_levels[level] = bullet_text_tag
            return bullet_text_tag

    def insert_bullet(self, line, level):
        # First remove any bullets on the line
        self.remove_bullet(line)
        logger.debug(f'Inserting bullet: {line=} {level=}')
        # Store the indentation level of the line
        self.set_ilevel(line, level)
        # Then insert the bullet char
        self.insert(f'{line}.0', f'{self.bullet_char}')
        # Then insert the bullet tag
        bullet_tag = self.bullet_tag(level)
        self.tag_add(bullet_tag, f'{line}.0', f'{line}.1')
        # Then insert the space
        self.insert(f'{line}.1', ' ')
        # Finally add the bulleted text tag for the whole new line
        bullet_text_tag = self.bullet_text_tag(level)
        self.tag_add(bullet_text_tag, f'{line}.1', f'{line}.end+1c')

    def remove_bullet(self, line):
        logger.debug(f'Removing bullet: {line=}')
        # Remove the bullet tag from the start of the line
        bullet_tag = self.bullet_tag(self.ilevel(line))
        self.tag_remove(bullet_tag, f'{line}.0', f'{line}.end')
        # Remove the bullet_text tag from the start of the line
        bullet_text_tag = self.bullet_text_tag(self.ilevel(line))
        self.tag_remove(bullet_text_tag, f'{line}.0', f'{line}.end+1c')
        # Delete any text on the line which would include the bullet and extra added space
        self.delete(f'{line}.0', f'{line}.end')
        # remove the indentation level of the line
        self.set_ilevel(line, 0)

    def apply_format(self, event: tk.Event):
        # current position - 1 (this is before insertion)
        position = self.index('insert')

        # convert line and character to int
        line = int(position.split('.')[0])
        col = int(position.split('.')[1])

        # Get all the tags for the current cursor position
        tags = self.tag_names(position)

        # Check if the user entered a bullet character at the start of a line
        if event.keysym in self.bullet_sym and col == 0:
            self.insert_bullet(line, self.ilevel(line))
        # Check if the user hit return
        elif event.keysym == 'Return':
            # Check if the user hit return on a bulleted line
            if any('bullet' in s for s in tags):
                # If the user hit return on a bulleted line and the return was the hit just after a previous return
                # meaning the user hit return twice, then get out of bulleted list mode.
                if col == 2:
                    self.remove_bullet(line)
                # Otherwise, just add a another bullet
                else:
                    self.insert(position, f'\n')
                    self.insert_bullet(line+1, self.ilevel(line))
            # If the user hit return when not in a bulleted line, just add a regular new line
            else:
                logger.debug(f'pos:{position} ilevel:{self.ilevel(line)}: Adding a regular old new line.')
                self.insert(position, f'\n')
        # Check if the user hit tab
        elif event.keysym == 'Tab':
            # Check if the user hit tab on a bulleted line
            if any('bullet' in s for s in tags):
                # If the user hit tab at the start an bulleted line, then indent it
                if col == 2:
                    self.insert_bullet(line, self.ilevel(line)+1)
        return 'break'
