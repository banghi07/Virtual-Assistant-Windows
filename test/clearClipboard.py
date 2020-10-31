import win32clipboard
win32clipboard.OpenClipboard()
win32clipboard.SetClipboardText("test")
s = win32clipboard.GetClipboardData()
print(s)
win32clipboard.EmptyClipboard()
win32clipboard.CloseClipboard()