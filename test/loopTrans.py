from googletrans import Translator
from pynput import mouse, keyboard
from pynput.keyboard import Key, Controller
import pyperclip
import time


keyboard = Controller()
translator = Translator()
chain = []


def on_move(x, y):
    global chain
    chain.append(2)


def on_click(x, y, button, pressed):
    global chain
    if pressed:
        chain.append(1)
    if not pressed:
        chain.append(3)

        if chain[-2] != 1:
            keyboard.press(Key.ctrl)
            keyboard.press("c")
            keyboard.release(Key.ctrl)
            keyboard.release("c")
            time.sleep(0.05)

            strFromClipBoard = pyperclip.paste()
            if strFromClipBoard == "":
                print("none")
            else:
                result = translator.translate(strFromClipBoard, dest="vi")
                print(result.text)

            pyperclip.copy("")


with mouse.Listener(on_move=on_move, on_click=on_click) as mouseListener:
    mouseListener.join()
