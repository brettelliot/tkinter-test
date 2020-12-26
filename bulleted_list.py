import tkinter as tk
from tkinter import font

global_root = tk.Tk()


class BulletedListText(tk.Text):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<KeyRelease>", self.on_key_pressed)

        text_font = font.nametofont(self.cget("font"))
        em = text_font.measure(" ")
        lmargin2 = em + text_font.measure("- ")
        self.tag_configure("bullet", lmargin1=em, lmargin2=lmargin2)

    def on_key_pressed(self, event):

        # After a space, this checks for a hyphen followed by a space on a new line and then
        # inserts 4 spaces.
        if event.char == ' ':
            last_char = self.get("insert-2c")
            if last_char == '-':
                line_start_pos = self.index("end-1c linestart")
                hyphen_pos = self.index("insert-2c")
                if line_start_pos == hyphen_pos:
                    # insert 4 spaces
                    # self.insert(line_start_pos, "    ", "bulleted")
                    self.tag_add("bullet", line_start_pos, "end")

class BulletedListText2(tk.Text):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #font metric
        fontname = self.cget("font").split()[0]
        # fontsize = self.cget("font").split()[1]
        child = font.Font(self, fontname).measure("- ")

        #tags
        self.tag_configure("parent", lmargin2=child)
        self.tag_configure("bullet", font=f'{fontname}')
        self.tag_configure("child",  lmargin1=child, lmargin2=child)

        #bullets
        self.bullet_chr = ['-', '.', '*', '+']
        self.bullet_sym = ['minus', 'period', 'asterisk', 'plus']

        #events
        for b in self.bullet_sym:
            self.bind(f'<KeyPress-{b}>', self.applyformat)

        self.bind('<KeyPress-Return>', self.applyformat)
        self.bind('<Control-Return>', self.applyformat)

    def applyformat(self, event:tk.Event):
        # current position - 1 (this is before insertion)
        position = self.index('insert')

        # convert line and character to int
        l = int(position.split('.')[0])
        c = int(position.split('.')[1])

        # apply formatting accordingly
        if event.keysym in self.bullet_sym and c == 0:                  ##bullet
            self.tag_remove("child", f'{l}.0-1c', 'end-1c')
            self.insert(position, f'{event.char} ')
            self.tag_add('bullet', f'{l}.0', f'{l}.1')
            self.tag_add('parent', f'{l}.1', 'end-1c')
            return 'break'
        elif event.keysym == 'Return':                                  ##sub
            if event.state & 0x4:
                self.insert(position, f'\n{Sub}')
                self.tag_add('child', f'{l+1}.0-1c', 'end')
            else:                                                       ##normal
                self.insert(position, f'\n')
                self.tag_remove('parent', f'{l+1}.0-1c', 'end')
                self.tag_remove("child", f'{l+1}.0-1c', 'end')
                self.tag_remove("bullet", f'{l+1}.0-1c', 'end')

            self.see(self.index('insert+1l'))
            return 'break'


class MyApp:

    def __init__(self, root):
        # Create the app
        self.root = root
        self.root.title("Bulleted list")

        # Set the main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both", side="top")

        # Create the text box
        self.text = BulletedListText(wrap="word", borderwidth=0, highlightthickness=0)
        self.text.pack(in_=self.main_frame, side="top", fill="both", expand=True)
        self.text.focus()

        # Kick off the main loop
        self.root.mainloop()


if __name__ == "__main__":
    app = MyApp(global_root)
