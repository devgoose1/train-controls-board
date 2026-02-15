"""
Test script to verify pyautogui can send keys to Railroader
This sends keys automatically - just keep Railroader focused
"""

import pyautogui
import time
import sys

print("=" * 70)
print("RAILROADER KEY PRESS TEST")
print("=" * 70)
print()
print("INSTRUCTIONS:")
print("1. Make sure Railroader window is visible")
print("2. Read the countdown below")
print("3. CLICK IN RAILROADER WINDOW during the countdown")
print("4. Keys will start sending automatically")
print("5. Watch the game and note what happens")
print()

# Countdown to let user focus window
print("Keys will start sending in:")
for i in range(5, 0, -1):
    print(f"  {i} seconds... (CLICK IN RAILROADER NOW!)", end='\r')
    time.sleep(1)

print("                                              ")
print()
print("Sending test keys NOW...")
print("=" * 70)
print()

# Test keys with delays
test_keys = [
    ('v', 'WHISTLE', 1, True),          # Hold for 1 second
    ('b', 'BELL', 0, False),            # Quick press
    ('j', 'HEADLIGHT UP', 0, False),
    ('-', 'THROTTLE UP', 0, False),
    ('k', 'CYLINDER COCKS', 0, False),
    ('[', 'REVERSER', 0, False),
]

for key, control, hold_time, is_hold in test_keys:
    print(f"  Sending: {control:25} (key '{key}')...", end='', flush=True)
    
    if is_hold:
        # For holding keys like whistle
        pyautogui.keyDown(key)
        time.sleep(hold_time)
        pyautogui.keyUp(key)
        print(f" [held for {hold_time}s]")
    else:
        # For momentary keys
        pyautogui.press(key)
        print(" [pressed]")
    
    time.sleep(0.7)  # Wait between tests

print()
print("=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print()
print("Did you see ANY controls activate in Railroader?")
print()

# For simulation mode, just show success
print("✓ If this is in SIMULATION mode, keys were sent successfully!")
print("✓ If nothing happened in Railroader, check:")
print()
print("  1. Railroader key bindings (Settings → Controls)")
print("     Make sure these keys are mapped:")
print("     - v, b, j, k, -, [, ], =, ', ;, ., ,")
print()
print("  2. Window mode:")
print("     Try windowed mode instead of fullscreen exclusive")
print()
print("  3. Administrator:")
print("     Run PowerShell as Administrator and try again")
print()
print("Run: python TROUBLESHOOTING.py for more help")
