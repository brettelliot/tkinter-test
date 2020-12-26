from pynput.keyboard import Key, Listener
import Quartz


class MyListener(Listener):

    def _event_to_key(self, event):
        my_dict = {}
        my_dict['CGEventGetType'] = Quartz.CGEventGetType(event)
        my_dict['kCGKeyboardEventAutorepeat'] = Quartz.CGEventGetIntegerValueField(
            event, Quartz.kCGKeyboardEventAutorepeat)
        my_dict['kCGKeyboardEventKeycode'] = Quartz.CGEventGetIntegerValueField(
            event, Quartz.kCGKeyboardEventKeycode)
        my_dict['kCGKeyboardEventKeyboardType'] = Quartz.CGEventGetIntegerValueField(
            event, Quartz.kCGKeyboardEventKeyboardType)

        print('\n')
        print("New _event_to_key call:")
        print(my_dict)

        return Listener._event_to_key(self, event)


def on_press(key):
    # print('> {} ({})'.format(str(key), listener.canonical(key)))
    pass


def on_release(key):
    # print('< {} ({})'.format(str(key), listener.canonical(key)))
    # if key == Key.esc:
    #     return False
    pass

with MyListener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()