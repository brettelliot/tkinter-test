# // Imports
import tkinter, pynput
from tkinter import messagebox

# // Global variables
root = tkinter.Tk()
app_title = "Tkinter and Pynput"
app_size = (300, 150)
listener_stop = False


# // Logics Keyboard
class Keyboard:
    # On button pressed
    def Pressed(key):
        # If listener_stop is True then stop listening
        if listener_stop == True: print("Keyboard Events are stoped!"); return False
        # Else show pressed key
        else: print(f"Keyboard pressed: {key}")

    # On button released
    def Released(key):
        print(f"Keyboard released: {key}")

    # Listen keybboard buttons
    def Listener():
        k_listen = pynput.keyboard
        k_listen.start()


# // Logics Mouse
class Mouse:
    # On move
    def Move(x, y):
        # If listener_stop is True then stop listening
        if listener_stop == True: print("Mouse Events are stoped!"); return False
        else: print(f"Mouse: Moved to {x}x{y}")

    # On scroll
    def Scroll(x, y, dx, dy):
        where = "down" if dy < 0 else "up"
        print(f"Mouse: Scrolled {where} at {x}x{y}")

    # On click
    def Click(x, y, button, pressed):
        action = "pressed" if pressed else "released"
        print(f"Mouse: {button} was {action} at {x}x{y}")

    # Listen keybboard buttons
    def Listener():
        m_listen = pynput.mouse
        m_listen.start()


# // Logics Define GUI
class MainApp:
    def __init__(self, master):
        self.master = master

        # Create tkinter interface
        X = int((master.winfo_screenwidth() - app_size[0]) / 2)
        Y = int((master.winfo_screenheight() - app_size[1]) / 2)
        master.wm_title(app_title)
        master.wm_geometry(f"{app_size[0]}x{app_size[1]}+{X}+{Y}")

        # Magic hapen here :P
        MainApp.Screen(master)
        MainApp.InputEvents()

    # Define Screen Informations
    def Screen(frame):
        # Set the main frame
        frame_main = tkinter.Frame(frame)
        frame_main.pack(expand=1, fill="x", side="top")

        # Defain frame components
        title = tkinter.Label(frame_main, text=app_title, font=("Comic Sans MS", 18, "bold"), fg="tomato")
        title.pack(expand=0, fill="x", side="top")

    # Input events
    def InputEvents():
        Keyboard.Listener()
        # Mouse.Listener()

    # Safe Quit
    def SafeQuit():
        global listener_stop

        if messagebox.askokcancel(f"{app_title} Quit", f"Are you shore you want to quit {app_title}?"):
            # We need to make shore if the window was closed and
            # listening event are still runing, then make them stop
            # You will see in fact they are not stoped (from console point view)
            # for that reason we check listener_stop on Mouse Move and on Keyboard Key press.
            # If for some reason the app is quit and listener has not stoped then on first action did will stop
            # Mouse move after app quit >> Mouse listener will stop
            # Keyboard button pressed after app quit >> Keyboard listener will stops
            if listener_stop == False:
                listener_stop = True
                print("Events Listening are stoped!")
            root.destroy()

# // Run if this is tha main file
if __name__ == "__main__":
    MainApp(root)
    root.protocol("WM_DELETE_WINDOW", MainApp.SafeQuit)
    root.mainloop()