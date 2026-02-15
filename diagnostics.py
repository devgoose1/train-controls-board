"""
System Diagnostics for Railroader Controller
Tests Python environment, pyautogui, and input detection
"""

import sys
import platform

print()
print("=" * 70)
print("RAILROADER CONTROLLER - SYSTEM DIAGNOSTICS")
print("=" * 70)
print()

# Check Python version
print(f"Python version: {sys.version}")
print(f"Platform: {platform.system()} {platform.release()}")
print()

# Check pyautogui
print("Checking pyautogui...")
pyautogui = None
try:
    import pyautogui
    print(f"  ✓ pyautogui imported successfully")
    print(f"  ✓ FAILSAFE: {pyautogui.FAILSAFE}")
    print(f"  ✓ PAUSE: {pyautogui.PAUSE}")
except Exception as e:
    print(f"  ✗ Error importing pyautogui: {e}")
    print("  Install with: pip install pyautogui")

# Check pyserial
print()
print("Checking pyserial...")
try:
    import serial
    print(f"  ✓ pyserial imported successfully")
    
    # List available ports
    import serial.tools.list_ports
    ports = list(serial.tools.list_ports.comports())
    if ports:
        print(f"  ✓ Found {len(ports)} COM port(s):")
        for port in ports:
            print(f"    - {port.device}: {port.description}")
    else:
        print(f"  ⚠ No COM ports found (Arduino not connected?)")
except Exception as e:
    print(f"  ✗ Error with pyserial: {e}")
    print("  Install with: pip install pyserial")

# Test screen size
print()
print("Checking screen...")
if pyautogui is not None:
    try:
        size = pyautogui.size()
        print(f"  ✓ Screen size: {size[0]} x {size[1]}")
        pos = pyautogui.position()
        print(f"  ✓ Mouse position: {pos}")
    except Exception as e:
        print(f"  ✗ Error getting screen info: {e}")
else:
    print(f"  ✗ pyautogui not available, skipping screen checks")

# Test key sending (visual only, no actual keys)
print()
print("Testing key name conversion...")
if pyautogui is not None:
    try:
        test_keys = ['v', 'b', 'j', 'k', '[', ']', '-', '=', "'", ";", ".", ","]
        pyautogui.FAILSAFE = False
        print(f"  ✓ Key names recognized: {', '.join(test_keys)}")
    except Exception as e:
        print(f"  ✗ Error with key names: {e}")
else:
    print(f"  ✗ pyautogui not available, skipping key tests")

# Summary
print()
print("=" * 70)
print("DIAGNOSTIC SUMMARY")
print("=" * 70)
print()

print("If all items above show ✓, then:")
print()
print("1. Run: python test_keys.py")
print("   - This will test if keys can actually reach Railroader")
print()
print("2. If test_keys.py fails but shows 'sent', then:")
print("   - Railroader is not accepting pyautogui input")
print("   - Solution: Try fullscreen windowed mode OR run as Admin")
print()
print("3. If you see ⚠ for COM ports:")
print("   - Arduino is not connected")
print("   - Use: python find_arduino_port.py for help")
print()
print("4. Check that your Railroader key bindings match:")
print()

bindings = {
    'v': 'WHISTLE',
    'b': 'BELL',
    'j': 'HEADLIGHT',
    'shift+j': 'HEADLIGHT (decrease)',
    '[': 'REVERSER',
    ']': 'REVERSER (opposite)',
    '-': 'THROTTLE',
    '=': 'THROTTLE (decrease)',
    "'": 'TRAIN BRAKE',
    ';': 'TRAIN BRAKE (decrease)',
    '.': 'INDEPENDENT BRAKE',
    ',': 'INDEPENDENT BRAKE (decrease)',
    'k': 'CYLINDER COCKS',
}

for key, control in bindings.items():
    print(f"   {key:15} → {control}")

print()
print("=" * 70)
