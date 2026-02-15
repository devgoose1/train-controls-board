"""
Test script using pynput instead of pyautogui
Pynput works better with some fullscreen games
"""

from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

print("=" * 70)
print("RAILROADER KEY PRESS TEST (PYNPUT VERSION)")
print("=" * 70)
print()
print("INSTRUCTIONS:")
print("1. Make sure Railroader window is visible")
print("2. CLICK IN RAILROADER WINDOW during the countdown")
print("3. Keys will start sending automatically")
print()

# Countdown
print("Keys will start sending in:")
for i in range(5, 0, -1):
    print(f"  {i} seconds... (CLICK IN RAILROADER NOW!)", end='\r')
    time.sleep(1)

print("                                              ")
print()
print("Sending test keys NOW...")
print("=" * 70)
print()

# Test keys
test_keys = [
    ('v', 'WHISTLE', 1.0, True),
    ('b', 'BELL', 0, False),
    ('j', 'HEADLIGHT UP', 0, False),
    ('-', 'THROTTLE UP', 0, False),
    ('k', 'CYLINDER COCKS', 0, False),
    ('[', 'REVERSER', 0, False),
]

for key, control, hold_time, is_hold in test_keys:
    print(f"  Sending: {control:25} (key '{key}')...", end='', flush=True)
    
    if is_hold:
        keyboard.press(key)
        time.sleep(hold_time)
        keyboard.release(key)
        print(f" [held for {hold_time}s]")
    else:
        keyboard.press(key)
        keyboard.release(key)
        print(" [pressed]")
    
    time.sleep(0.7)

print()
print("=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print()
print("Did you see ANY controls activate in Railroader?")
print()
print("If YES: Great! We'll convert the main controller to use pynput")
print("If NO: There might be a deeper Windows/game compatibility issue")
print()
