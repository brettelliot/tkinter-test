from jaraco import clipboard

text_sammple = 'some text'
html_sample = '<p>Your paragraph here</p>'

def test_copy_text():
    clipboard.copy_text(text_sammple)

def test_paste_text():
    assert clipboard.paste_text() == text_sammple

def test_copy_html():
    clipboard.copy_html(html_sample)

def test_paste_html():
    assert clipboard.paste_html() == html_sample

def print_text_from_clipboard():
    print(clipboard.paste_text())

def print_html_from_clipboard():
    print(clipboard.paste_html())

if __name__ == '__main__':
    test_copy_text()
    # test_paste_text()
    # test_copy_html()
    # test_paste_html()
    print_html_from_clipboard()
    print_text_from_clipboard()
