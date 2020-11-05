import pyperclip
import time
from pynput import keyboard, mouse
from pynput.keyboard import Controller, Key
from googletrans import Translator

while True:
    keyboard = Controller()
    translator = Translator()
    result = ""
    chain = []

    def on_move(x, y):
        global chain
        chain.append(2)

    def on_click(x, y, button, pressed):
        global chain
        if pressed:
            chain.append(1)
        else:
            chain.append(3)
            return False

    with mouse.Listener(on_move=on_move, on_click=on_click) as mouseListener:
        mouseListener.join()

    if chain[-2] != 1:
        keyboard.press(Key.ctrl)
        keyboard.press("c")
        keyboard.release(Key.ctrl)
        keyboard.release("c")
        time.sleep(0.05)

        str_from_clipboard = pyperclip.paste()

        if str_from_clipboard != "":
            try:
                content = translator.translate(
                    str(str_from_clipboard), dest="vi")
            except:
                print("loi")
            else:
                result = "[Nguồn] {0}\n[Đích] {1}\n[Kết quả]\n{2}".format(
                    content.src, content.dest, content.text)
                print(result)
                pyperclip.copy("")
