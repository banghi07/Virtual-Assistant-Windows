import win32ui
while True:
    wnd = win32ui.GetForegroundWindow()
    print("{}\n".format(wnd.GetWindowText()))