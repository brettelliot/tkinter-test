import unittest
import tkinter as tk


class TKTestCase(unittest.TestCase):
    """These methods are going to be the same for every GUI test,
    so refactored them into a separate class
    """
    def setUp(self):
        self.root = tk.Tk()
        self.pump_events()

    def tearDown(self):
        if self.root:
            self.root.destroy()
            self.pump_events()

    def pump_events(self):
        while self.root.dooneevent(tk._tkinter.ALL_EVENTS | tk._tkinter.DONT_WAIT):
            pass


class TestText(TKTestCase):

    def test_insert_text_with_newline(self):
        text = tk.Text(self.root, width=40, height=15)
        text.pack(fill="both", expand=True)
        self.pump_events()
        text.focus_set()

        starting_position = text.index('insert')
        self.assertEqual("1.0", starting_position)

        text.insert(starting_position, "Newline test\n")
        # text.event_generate('<Return>')
        self.pump_events()

        actual_position = text.index('insert')
        self.assertEqual("2.0", actual_position)

if __name__ == "__main__":
    unittest.main()