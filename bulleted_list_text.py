import tkinter as tk
from tkinter import font
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.ERROR)


class BulletedListText(tk.Text):
    """
    The BulletedListText widget adds simple bulleted list functionality to the standard text widget.

    To create a bulleted list, enter a bullet character (asterisk, minus, or plus) and then a space at the start of a
    new line. The text on the bulleted line soft wraps and is indented to align with the first char in the bulleted
    line. Add more bullets simply by hitting return. You can indent sub-bullets by hitting the tab button at the
    beginning of a bullet.  You can un-indent sub-bullets by hitting the return key, once for each level until you
    exit from the bulleted list.

    Todo for the bulleted list text widget:
    * The lmargin2 doesn't align with the second space.
    * When hitting tab at the start of a non-empty bullet, don't delete the text from the line. just indent.
    * When hitting enter at the middle of a non-empty bullet, don't delete the text from the line. just start a
    new bullet with that text.

    Todo for bullet pad:
    * Add undo and redo
    * Auto scroll when adding text at the bottom of the widget
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # tags
        self.bullet_char = '-'
        self.num_spaces_per_indent = 4
        self.num_spaces_after_bullet = 2
        font_name = font.nametofont(self.cget("font"))
        self.indent_width = font_name.measure(self.num_spaces_per_indent * ' ')
        self.bullet_width = font_name.measure(f'{self.bullet_char}{self.num_spaces_after_bullet *" "}')

        # events
        self.bullet_sym = ['minus', 'asterisk', 'plus']
        for b in self.bullet_sym:
            self.bind(f'<KeyPress-{b}>', self.apply_format)
        self.bind('<KeyPress-Return>', self.apply_format)
        self.bind('<KeyPress-Tab>', self.apply_format)
        self.bind('<KeyPress-BackSpace>', self.on_backspace)
        self.bind('<KeyPress-Delete>', self.on_backspace)

        # book keeping
        self.bullet_tag_levels = {}
        self.bullet_text_tag_levels = {}

    def level_from_tags(self, tags):
        level_set = set()
        for tag in tags:
            if 'bullet_l' in tag:
                level_string = tag[8:]
                level_set.add(int(level_string))
            elif 'bullet_text_l' in tag:
                level_string = tag[13:]
                level_set.add(int(level_string))
        if len(level_set) == 0:
            return 0
        elif len(level_set) == 1:
            return level_set.pop()
        else:
            logger.error(f'Detected line with bullet tags from multiple levels: {tags}')
            return min(level_set)

    def bullet_tag(self, level):
        if level < 1:
            return ''
        elif level in self.bullet_tag_levels:
            return self.bullet_tag_levels[level]
        else:
            bullet_tag = f'bullet_l{level}'
            if logging.DEBUG >= logger.level:
                self.tag_configure(
                    bullet_tag,
                    # how much to indent the first line of a chunk of text
                    lmargin1=self.indent_width * level,
                    background='red')
            else:
                self.tag_configure(
                    bullet_tag,
                    # how much to indent the first line of a chunk of text
                    lmargin1=self.indent_width * level)
            self.bullet_tag_levels[level] = bullet_tag
            return bullet_tag

    def bullet_text_tag(self, level):
        if level < 1:
            return ''
        elif level in self.bullet_text_tag_levels:
            return self.bullet_text_tag_levels[level]
        else:
            bullet_text_tag = f'bullet_text_l{level}'
            if logging.DEBUG >= logger.level:
                self.tag_configure(
                    bullet_text_tag,
                    # how much to indent the first line of a chunk of text
                    lmargin1=(self.indent_width * level),
                    # lmargin1=(self.two_spaces),
                    # how much to indent successive lines of a chunk of text
                    lmargin2=(self.indent_width * level) + self.bullet_width,
                    # lmargin2=(self.indent_width * level) + self.three_spaces,
                    background='green')

            else:
                self.tag_configure(
                    bullet_text_tag,
                    # how much to indent the first line of a chunk of text
                    lmargin1=(self.indent_width * level),
                    # how much to indent successive lines of a chunk of text
                    lmargin2=(self.indent_width * level) + self.bullet_width)
            self.bullet_text_tag_levels[level] = bullet_text_tag
            return bullet_text_tag

    def insert_bullet(self, line, level):
        # If we're inserting a bullet of level zero that means we're just removed all bullets on the line.
        if level == 0:
            return
        elif level < 0:
            logger.error(f'insert_bullet: being called with {line=} {level=}')
            return
        logger.debug(f'Inserting bullet: {line=} {level=}')
        # Then insert the bullet char
        self.insert(f'{line}.0', f'{self.bullet_char}')
        # Then insert the bullet tag
        bullet_tag = self.bullet_tag(level)
        self.tag_add(bullet_tag, f'{line}.0', f'{line}.1')
        # Then insert the spaces after the bullet
        self.insert(f'{line}.1', f'{self.num_spaces_after_bullet * " "}')
        # Finally add the bulleted text tag for the whole new line
        bullet_text_tag = self.bullet_text_tag(level)
        self.tag_add(bullet_text_tag, f'{line}.1', f'{line}.end+1c')

    def remove_bullet(self, line, level):
        logger.debug(f'Removing bullet: {line=} {level=}')
        # Remove the bullet tag from the start of the line
        bullet_tag = self.bullet_tag(level)
        self.tag_remove(bullet_tag, f'{line}.0', f'{line}.1')
        # Remove the bullet_text tag from the whole line
        bullet_text_tag = self.bullet_text_tag(level)
        self.tag_remove(bullet_text_tag, f'{line}.0', f'{line}.end+1c')
        # Delete any text on the line which would include the bullet and extra added space
        self.delete(f'{line}.0', f'{line}.end')

    def apply_format(self, event: tk.Event):
        # current position - 1 (this is before insertion)
        position = self.index('insert')

        # convert line and character to int
        line = int(position.split('.')[0])
        col = int(position.split('.')[1])

        # Get all the tags for the current cursor position
        tags = self.tag_names(position)
        level = self.level_from_tags(tags)

        # Check if the user entered a bullet character at the start of a line
        if event.keysym in self.bullet_sym and col == 0:
            self.insert_bullet(line, 1)
        # Check if the user hit return
        elif event.keysym == 'Return':
            # Check if the user hit return on a bulleted line
            if level > 0:
                # If the user hit return on a bulleted line and the return was the hit just after a previous return
                # meaning the user hit return twice, reduce the indentation level of that line (possibly ending
                # the bulleted list).
                if col == self.num_spaces_after_bullet + 1:
                    # First remove any bullets on the line
                    self.remove_bullet(line, level)
                    self.insert_bullet(line, level-1)
                # Otherwise, just add a another bullet
                else:
                    self.insert(position, f'\n')
                    self.remove_bullet(line+1, level)
                    self.insert_bullet(line+1, level)
            # If the user hit return when not in a bulleted line, just add a regular new line
            else:
                logger.debug(f'{position=} {level=} Adding a regular old new line.')
                self.insert(position, f'\n')
        # Check if the user hit tab
        elif event.keysym == 'Tab':
            # Check if the user hit tab on a bulleted line
            if level > 0:
                # If the user hit tab at the start an bulleted line, then indent it
                if col == self.num_spaces_after_bullet + 1:
                    self.remove_bullet(line, level)
                    self.insert_bullet(line, level+1)
        return 'break'

    def on_backspace(self, event):
        # current position - 1 (this is before insertion)
        position = self.index('insert')

        # convert line and character to int
        line = int(position.split('.')[0])
        col = int(position.split('.')[1])

        # Get all the tags for the current cursor position
        tags = self.tag_names(position)
        level = self.level_from_tags(tags)

        if any("bullet" in s for s in tags):
            if col in [0,1,2,3]:
                if level > 0:
                    # If the user hit backspace on a bulleted line and the cursor is one of the
                    # bulleted characters then don't delete the character but un-indent
                    self.remove_bullet(line, level)
                    self.insert_bullet(line, level-1)
                    return 'break'
