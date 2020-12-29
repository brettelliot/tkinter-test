import tkinter as tk
from tkinter import font
import logging

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.ERROR)


class BulletedListText(tk.Text):
    """
    The BulletedListText widget adds simple bulleted list functionality to the standard text widget.

    To create a bulleted list, enter a bullet character (asterisk, minus, or plus) and then a space at the start of a
    new line. The text on the bulleted line soft wraps and is indented to align with the first char in the bulleted
    line. Add more bullets simply by hitting return. You can indent sub-bullets by hitting the tab button at the
    beginning of a bullet.  You can un-indent sub-bullets by hitting the return key, once for each level until you
    exit from the bulleted list.

    Todo for the bulleted list text widget:
    * handle a font change (probs need to reset the *.width properties and recreate the tags).
    * clicking into the bullet character area should move the cursor to the first character after the bullet chars
    * shift tab should un-indent without messing the lines text
    * Unit tests for this biatch
    * If you're under a bulleted line but not on a bulleted line and you backspace and end up at the end of the bulleted
     line then if you hit enter, it should create a new bullet.
     * Hitting cmd and left arrow on a bulleted line takes me to the front of the bulleted chars. It should take me to
     the end of the bulleted chars (ie: where I can start editing).

    Todo for bullet pad:
    * Add undo and redo
    * Auto scroll when adding text at the bottom of the widget
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # bullet stuff
        # The character for the bullet
        self.bullet_char = '-'
        # The number of spaces to put after the bullet character before the text on the bulleted line
        self.num_spaces_after_bullet = 2
        # The column number where the last of the bullet characters are
        self.bullet_chars_end_col = len(f'{self.bullet_char}{self.num_spaces_after_bullet * " "}')
        logger.debug(f'{self.bullet_chars_end_col=}')
        # The number of spaces for each indent level
        self.num_spaces_per_indent = 4

        # font stuff
        text_font = font.nametofont(self.cget("font"))
        self.indent_width = text_font.measure(f'{self.num_spaces_per_indent * " "}')
        self.bullet_width = text_font.measure(f'{self.bullet_char}{self.num_spaces_after_bullet * " "}')

        # events
        self.bullet_sym = ['minus', 'asterisk', 'plus']
        self.bind('<KeyPress>', self.on_keypress)

        # book keeping
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

    def bullet_text_tag(self, level):
        if level < 1:
            return ''
        elif level in self.bullet_text_tag_levels:
            return self.bullet_text_tag_levels[level]
        else:
            bullet_text_tag = f'bullet_text_l{level}'
            # how much to indent the first line of a bulleted line
            lmargin1 = (self.indent_width * level)
            # how much to indent successive lines of a bulleted line
            lmargin2 = (self.indent_width * level) + self.bullet_width
            if logging.DEBUG >= logger.level:
                self.tag_configure(bullet_text_tag, lmargin1=lmargin1, lmargin2=lmargin2, background='green')
            else:
                self.tag_configure(bullet_text_tag, lmargin1=lmargin1, lmargin2=lmargin2)
            self.bullet_text_tag_levels[level] = bullet_text_tag
            return bullet_text_tag

    def insert_bullet(self, line, level):
        # If we're inserting a bullet of level zero that means we're just removed all bullets on the line.
        if level == 0:
            return
        elif level < 0:
            logger.error(f'  insert_bullet: being called with {line=} {level=}')
            return

        # Insert the bullet char and spaces, then tag the line with bullet_text_tag
        logger.debug(f'  insert_bullet: {line=} {level=}')
        bullet_text_tag = self.bullet_text_tag(level)
        self.insert(f'{line}.0', f'{self.bullet_char}{self.num_spaces_after_bullet * " "}')
        self.tag_add(bullet_text_tag, f'{line}.0', f'{line}.end+1c')

    def remove_bullet(self, line, level):
        logger.debug(f'  remove_bullet: {line=} {level=}')
        bullet_text_tag = self.bullet_text_tag(level)
        self.tag_remove(bullet_text_tag, f'{line}.0', f'{line}.end+1c')
        # Delete any text on the line which would include the bullet and extra added space
        self.delete(f'{line}.0', f'{line}.{self.bullet_chars_end_col}')

    def on_keypress(self, event: tk.Event):
        # current position - 1 (this is before insertion)
        position = self.index('insert')
        logger.debug(f'{position}: on_keypress')

        # convert line and character to int
        line = int(position.split('.')[0])
        col = int(position.split('.')[1])

        # Get all the tags for the current cursor position
        tags = self.tag_names(position)
        level = self.level_from_tags(tags)

        # Check if the user entered a bullet character at the start of a line
        if event.keysym in self.bullet_sym and col == 0:
            self.insert_bullet(line, 1)
            return 'break'

        # Check if the user hit return
        elif event.keysym == 'Return':
            # Check if the user hit return on a bulleted line
            if level > 0:
                # If the user hit return on a bulleted line and the return was the hit just after a previous return
                # meaning the user hit return twice, reduce the indentation level of that line (possibly ending
                # the bulleted list).
                if col <= self.bullet_chars_end_col:
                    # First remove any bullets on the line
                    self.remove_bullet(line, level)
                    self.insert_bullet(line, level - 1)
                    return 'break'
                # Otherwise, just add a another bullet
                else:
                    self.insert(position, f'\n')
                    self.insert_bullet(line + 1, level)
                    return 'break'
            # If the user hit return when not in a bulleted line, just add a regular new line
            else:
                self.insert(position, f'\n')
                return 'break'

        # Check if the user hit tab
        elif event.keysym == 'Tab':
            # Check if the user hit tab on a bulleted line
            if level > 0:
                # If the user hit tab at the start an bulleted line, then indent it
                if col <= self.bullet_chars_end_col:
                    self.remove_bullet(line, level)
                    self.insert_bullet(line, level + 1)
                    return 'break'

        # check if user hit backspace
        elif event.keysym == 'BackSpace':
            if any("bullet" in s for s in tags):
                if col <= self.bullet_chars_end_col:
                    if level > 0:
                        # If the user hit backspace on a bulleted line and the cursor is one of the
                        # bulleted characters then don't delete the character but un-indent
                        self.remove_bullet(line, level)
                        self.insert_bullet(line, level - 1)
                        return 'break'

        elif event.keysym == 'Left':
            if level > 0 and col <= self.bullet_chars_end_col:
                # Someones used the left arrow to access the bullet character space. Don't let them
                self.mark_set('insert', f'{line}.{self.bullet_chars_end_col}')
                return 'break'

        # Any other keypress
        else:
            if level > 0 and col < self.bullet_chars_end_col:
                # Someones typing in the bullet character space. Don't let them
                self.mark_set('insert', f'{line}.{self.bullet_chars_end_col}')
                return 'break'

