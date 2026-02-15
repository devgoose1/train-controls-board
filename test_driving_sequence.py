"""
Railroader Driving Sequence Test
Performs a realistic driving sequence instead of random values
Perfect for testing all controls in a logical order
"""

from pynput.keyboard import Key, Controller
import time
import ctypes

# ============================================================================
# CONFIGURATION
# ============================================================================

WINDOW_NAME = "Railroader"
SEQUENCE_DELAY = 2  # Seconds between each step
LOG_KEYS = True

keyboard = Controller()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_active_window_title():
    """Get the title of the currently active window"""
    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
        return buff.value
    except:
        return ""

def is_railroader_focused():
    """Check if Railroader is focused"""
    title = get_active_window_title()
    return WINDOW_NAME.lower() in title.lower() if title else False

def press_key(key, hold_duration=0.15):
    """Press and hold a key"""
    if not is_railroader_focused():
        print("  ⚠ Railroader not focused - skipping key press!")
        return
    
    keyboard.press(key)
    if hold_duration > 0:
        time.sleep(hold_duration)
    keyboard.release(key)

def press_hotkey(modifier, key):
    """Press a key combination"""
    if not is_railroader_focused():
        print("  ⚠ Railroader not focused - skipping key press!")
        return
    
    keyboard.press(modifier)
    keyboard.press(key)
    keyboard.release(key)
    keyboard.release(modifier)

def log_step(step_num, description):
    """Log a step in the sequence"""
    print()
    print("=" * 70)
    print(f"STEP {step_num}: {description}")
    print("=" * 70)

def press_multiple(key, count, description):
    """Press a key multiple times"""
    print(f"  Pressing '{key}' {count} times ({description})...")
    for i in range(count):
        press_key(key)
        time.sleep(0.1)
    print(f"  ✓ Completed: {description}")

# ============================================================================
# DRIVING SEQUENCE
# ============================================================================

def run_driving_sequence():
    """Execute a realistic train driving sequence"""
    
    print()
    print("=" * 70)
    print("RAILROADER DRIVING SEQUENCE TEST")
    print("=" * 70)
    print()
    print("This will perform a realistic driving sequence:")
    print("  1. Set all brakes to OFF")
    print("  2. Reverser to FULL FORWARD")
    print("  3. Throttle UP gradually")
    print("  4. Reverser to 50% FORWARD")
    print("  5. Throttle to OFF")
    print("  6. Brakes to FULL ON")
    print()
    print("Make sure Railroader is focused!")
    print()
    
    # Countdown
    for i in range(5, 0, -1):
        print(f"Starting in {i} seconds... (CLICK IN RAILROADER NOW!)", end='\r')
        time.sleep(1)
    
    print("                                                        ")
    print()
    
    if not is_railroader_focused():
        print("✗ ERROR: Railroader is not focused!")
        print("Please click in the Railroader window and try again.")
        return
    
    print("✓ Railroader detected - Starting sequence!")
    print()
    time.sleep(1)
    
    # STEP 1: Release all brakes
    log_step(1, "RELEASE ALL BRAKES")
    print("  Setting train brake to minimum...")
    press_multiple(';', 20, "Train brake OFF")
    time.sleep(0.5)
    print("  Setting independent brake to minimum...")
    press_multiple(',', 20, "Independent brake OFF")
    time.sleep(SEQUENCE_DELAY)
    
    # STEP 2: Reverser full forward
    log_step(2, "REVERSER FULL FORWARD")
    press_multiple('[', 20, "Reverser to full forward")
    time.sleep(SEQUENCE_DELAY)
    
    # STEP 3: Throttle up gradually
    log_step(3, "THROTTLE UP GRADUALLY")
    print("  Increasing throttle to 50%...")
    press_multiple('-', 10, "Throttle to 50%")
    time.sleep(SEQUENCE_DELAY)
    
    print("  Increasing throttle to 100%...")
    press_multiple('-', 10, "Throttle to 100%")
    time.sleep(SEQUENCE_DELAY * 2)  # Let it run at full throttle
    
    # STEP 4: Reverser to 50%
    log_step(4, "REVERSER TO 50% FORWARD")
    press_multiple(']', 10, "Reverser to 50%")
    time.sleep(SEQUENCE_DELAY)
    
    # STEP 5: Throttle off
    log_step(5, "THROTTLE TO ZERO")
    press_multiple('=', 20, "Throttle OFF")
    time.sleep(SEQUENCE_DELAY)
    
    # STEP 6: Apply brakes
    log_step(6, "APPLY BRAKES")
    print("  Applying independent brake...")
    press_multiple('.', 10, "Independent brake to 50%")
    time.sleep(1)
    
    print("  Applying train brake...")
    press_multiple("'", 15, "Train brake to 75%")
    time.sleep(1)
    
    print("  Full emergency braking!")
    press_multiple("'", 5, "Train brake to 100%")
    press_multiple('.', 10, "Independent brake to 100%")
    time.sleep(SEQUENCE_DELAY)
    
    # BONUS: Test other controls
    log_step(7, "TEST OTHER CONTROLS")
    print("  Testing headlight...")
    press_key('j')
    time.sleep(0.5)
    press_key('j')
    time.sleep(0.5)
    print("  ✓ Headlight tested")
    
    print("  Testing bell...")
    press_key('b')
    time.sleep(1)
    press_key('b')
    time.sleep(0.5)
    print("  ✓ Bell tested")
    
    print("  Testing whistle low...")
    press_key('h')
    time.sleep(1)
    print("  ✓ Whistle low tested")
    
    print("  Testing whistle high...")
    press_hotkey(Key.shift, 'h')
    time.sleep(1)
    print("  ✓ Whistle high tested")
    
    print("  Testing cylinder cocks...")
    press_key('k')
    time.sleep(0.5)
    press_key('k')
    time.sleep(0.5)
    print("  ✓ Cylinder cocks tested")
    
    # Completed
    print()
    print("=" * 70)
    print("DRIVING SEQUENCE COMPLETE!")
    print("=" * 70)
    print()
    print("✓ All controls have been tested in a realistic sequence.")
    print("✓ If everything worked, your train should now be stopped.")
    print()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    try:
        run_driving_sequence()
    except KeyboardInterrupt:
        print("\n\n⚠ Sequence interrupted by user")
    except Exception as e:
        print(f"\n\n✗ Error: {e}")
    finally:
        print("\n✓ Test complete")
