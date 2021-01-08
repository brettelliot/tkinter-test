import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk, ImageChops, ImageDraw


class RichText(tk.Text):
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

        lmargin2 = em + default_font.measure("\u2022 ")
        self.tag_configure("bullet", lmargin1=em, lmargin2=lmargin2)

    def insert_bullet(self, index, text):
        self.insert(index, f"\u2022 {text}", "bullet")



def callback():
    print("called the callback!")



def crop_to_circle(im):
    # bigsize = (im.size[0] * 3, im.size[1] * 3)
    # mask = Image.new('L', bigsize, 0)
    # ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
    # mask = mask.resize(im.size, Image.ANTIALIAS)
    # mask = ImageChops.darker(mask, im.split()[-1])
    # im.putalpha(mask)
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    # mask = ImageChops.darker(mask, im.split()[-1])
    im.putalpha(mask)



if __name__ == "__main__":

    root = tk.Tk()
    text = RichText(root, width=40, height=15)
    text.pack(fill="both", expand=True)

    text.insert("end", "Toolbar Example\n", "h1")
    text.insert("end", "Hello, world\n\n")

    text.insert("end", "\n")
    text.insert("end", "This line is bold\n", "bold")
    text.insert("end", "This line is italicized\n", "italic")

    # Load all the images first as PNGs and use ImageTk to convert
    # them to usable Tkinter images.
    list_img = Image.open(r'resources/icons/list.png').convert('RGBA')
    crop_to_circle(list_img)
    list_img = list_img.resize((24, 24), Image.ANTIALIAS)
    list_icon = ImageTk.PhotoImage(list_img)
    gear_img = Image.open(r'resources/icons/gear.png').convert('RGBA')
    crop_to_circle(gear_img)
    gear_img = gear_img.resize((24, 24), Image.ANTIALIAS)
    gear_icon = ImageTk.PhotoImage(gear_img)

    # create a toolbar
    toolbar = tk.Frame(root, relief='flat', height=24)
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    b = tk.Button(toolbar, relief=tk.FLAT, compound = tk.LEFT, command=callback, image=list_icon)
    b.pack(side=tk.LEFT, padx=0, pady=0)

    b = tk.Button(toolbar, compound = tk.RIGHT, command=callback, relief=tk.FLAT, image=gear_icon)
    b.pack(side=tk.RIGHT, padx=0, pady=0)



    root.mainloop()
