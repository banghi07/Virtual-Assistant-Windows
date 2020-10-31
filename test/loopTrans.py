from PyQt5.QtWidgets import QApplication
from googletrans import Translator
from pynput import mouse, keyboard
from pynput.keyboard import Key, Controller
import pyperclip
import win32clipboard
import time


kBoard = Controller()
translator = Translator()
# killMouseListener = False

# def on_release(key):
#     if key == keyboard.Key.esc:
#         killMouseListener = True
#         return False

# with keyboard.Listener(on_release=on_release) as keyBoardListener:
#     keyBoardListener.join()

# flagMousePressed  = False
# flagMouseRelease  = False
# flagMouseMove = False

# def on_move(x, y):
#     global flagMouseMove
#     flagMouseMove = True

# def on_click(x, y, button, pressed):
#     if pressed:
#         global flagMousePressed
#         flagMousePressed = True
#     else:
#         global flagMouseRelease 
#         flagMouseRelease = True
#         return False

def clearClipboard():
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()

def on_click(x, y, button, pressed):
    if not pressed:
        kBoard.press(Key.ctrl)
        kBoard.press("c")
        kBoard.release(Key.ctrl)
        kBoard.release("c")
        time.sleep(0.05)
        return False

count = 0;
while count < 100:
    oldClipboard = pyperclip.paste()
    print("1. old clipboard: " + oldClipboard)
    with mouse.Listener(on_click=on_click) as mouseListener:
        mouseListener.join()
    newClipboard = pyperclip.paste()
    print("2. new clipboard: " + newClipboard)
    print("3.")
    if newClipboard != oldClipboard:
        result = translator.translate(newClipboard, dest="vi")
        clearClipboard()
        print(result)
    else: 
        print("    none")
    print("==================================")
    count = count + 1


