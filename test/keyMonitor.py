from pynput import keyboard

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(on_release=on_release) as listener:
    listener.join()
