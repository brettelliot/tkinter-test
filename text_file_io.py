import tkinter as tk
from tkinter import font as tkFont
import pickle


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


if __name__ == "__main__":

    root = tk.Tk()
    text = RichText(root, width=40, height=15)
    text.pack(fill="both", expand=True)

    text.insert("end", "Rich Text Example\n", "h1")
    text.insert("end", "Hello, world\n\n")
    text.insert_bullet("end", "Item 1\n")
    text.insert_bullet("end", "Item 2\n")

    text.insert("end", "\n")
    text.insert("end", "This line is bold\n", "bold")
    text.insert("end", "This line is italicized\n", "italic")

    dumped_text_list = text.dump("1.0", "end", tag=True, text=True, mark=False)
    print(f'{dumped_text_list=}')
    with open('text_file_io.data', 'wb') as file_handle:
        # store the data as binary data stream
        pickle.dump(dumped_text_list, file_handle)

    text.delete('1.0', "end")

    with open('text_file_io.data', 'rb') as file_handle:
        # read the data as binary data stream
        loaded_text_list = pickle.load(file_handle)
        # print(type(loaded_text_list))
        # print(f'{loaded_text_list=}')
        # print(f'{loaded_text_list[0]}, {type(loaded_text_list[0])}')

        tag_name = ''
        for (key, value, index) in loaded_text_list:
            if key == 'tagon':
                tag_name = value
            elif key == 'text':
                text.insert(index, value)
                if tag_name != '':
                    ending_index = text.index('end -1c')
                    text.tag_add(tag_name, index, ending_index)
            elif key == 'tagoff':
                tag_name = ''

    dumped_text_list = text.dump("1.0", "end", tag=True, text=True, mark=False)
    print(f'{dumped_text_list=}')

    root.mainloop()
