import ctypes

# Define necessary constants
WMP_PLAYSTATE_STOPPED = 0x00000001
WMP_PLAYSTATE_PAUSED = 0x00000008
WMP_PLAYSTATE_PLAYING = 0x00000003

# Define necessary functions and structures
SendMessage = ctypes.windll.user32.SendMessageW
FindWindow = ctypes.windll.user32.FindWindowW

class COPYDATASTRUCT(ctypes.Structure):
    _fields_ = [
        ('dwData', ctypes.wintypes.DWORD),
        ('cbData', ctypes.wintypes.DWORD),
        ('lpData', ctypes.wintypes.LPVOID)
    ]

def pause_media():
    # Find the Windows Media Player window
    hwnd = FindWindow('WMPlayerApp', None)

    # Send the pause command to the Windows Media Player window
    cds = COPYDATASTRUCT()
    cds.dwData = WMP_PLAYSTATE_PAUSED
    cds.cbData = 0
    cds.lpData = None
    SendMessage(hwnd, 0x004A, 0, ctypes.byref(cds))

pause_media()