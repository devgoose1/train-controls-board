"""
Test Window Focus Detection
This will show you the active window title in real-time
"""

import ctypes
import time

def get_active_window_title():
    """Get the title of the currently active window (Windows only)"""
    try:
        # Get foreground window handle
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        
        # Get window title length
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        
        # Get window title
        buff = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
        
        return buff.value
    except Exception as e:
        return f"ERROR: {e}"


print("=" * 70)
print("WINDOW FOCUS DETECTION TEST")
print("=" * 70)
print()
print("This will show you the currently active window title.")
print("Click between different windows to test.")
print("Press Ctrl+C to stop.")
print()
print("-" * 70)
print()

try:
    last_title = ""
    while True:
        title = get_active_window_title()
        
        if title != last_title:
            print(f"Active window: '{title}'")
            
            # Check if Railroader is in the title
            is_railroader = "Railroader".lower() in title.lower() if title else False
            
            if is_railroader:
                print("  ✓✓✓ RAILROADER FOCUSED - Keys WILL be sent ✓✓✓")
            else:
                print("  ✗✗✗ NOT Railroader - Keys will be BLOCKED ✗✗✗")
            
            print()
            last_title = title
        
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\n\nTest stopped.")
    print()
    print("If you saw 'RAILROADER DETECTED' when clicking Railroader,")
    print("then window detection is working correctly!")
