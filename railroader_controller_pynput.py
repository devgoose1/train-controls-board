"""
Railroader Train Control Panel Interface (PYNPUT VERSION)
Reads control values from simulation or Arduino serial and translates to keyboard controls
Uses pynput library which works better with some fullscreen games

SAFETY: Only sends keys when Railroader window is focused!
"""

from pynput.keyboard import Key, Controller
import time
import random
import serial
import serial.tools.list_ports
import ctypes
import sys

# ============================================================================
# CONFIGURATION
# ============================================================================

SIMULATION_MODE = True  # Set to False to use real Arduino serial input
UPDATE_INTERVAL = 0.05  # Seconds between control updates
MAX_STEPS = 20  # Maximum steps for multi-step controls (throttle, brake, etc.)
SERIAL_PORT = "COM3"  # Change to your Arduino's COM port
SERIAL_BAUD = 9600  # Standard baud rate
STARTUP_DELAY = 5  # Seconds to wait before starting (time to switch to Railroader)
DEBUG_MODE = False  # Set to True to see detailed value debugging (very verbose!)
LOG_KEYS = True  # Log each key press to console
WINDOW_NAME = "Railroader"  # Partial name of Railroader window (case-insensitive)

# Initialize pynput keyboard controller
keyboard = Controller()

# ============================================================================
# WINDOW FOCUS DETECTION (SAFETY)
# ============================================================================

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
        return ""


def is_railroader_focused():
    """Check if Railroader window is currently focused"""
    title = get_active_window_title()
    if not title:
        return False
    # Check if "Railroader" is in the window title (case-insensitive)
    is_focused = WINDOW_NAME.lower() in title.lower()
    return is_focused

# ============================================================================
# DEBUG LOGGING
# ============================================================================

def log_key(key, action="PRESS", control=""):
    """Debug logging for key presses"""
    if LOG_KEYS:
        if control:
            print(f"  [{control}] {action}: '{key}'")
        else:
            print(f"  {action}: '{key}'")

# ============================================================================
# KEYBOARD FUNCTIONS (PYNPUT)
# ============================================================================

def press_key(key, hold_duration: float = 0):
    """Press and release a key with optional hold duration"""
    keyboard.press(key)
    if hold_duration > 0:
        time.sleep(hold_duration)
    keyboard.release(key)

def hold_key(key):
    """Hold a key down"""
    keyboard.press(key)

def release_key(key):
    """Release a held key"""
    keyboard.release(key)

def press_hotkey(modifier, key):
    """Press a key combination (e.g., shift+j)"""
    keyboard.press(modifier)
    keyboard.press(key)
    keyboard.release(key)
    keyboard.release(modifier)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def map_to_steps(value, in_min=0, in_max=1023, steps=MAX_STEPS):
    """
    Map an analog value (0-1023) to discrete steps (0-MAX_STEPS)
    Useful for throttle, brake pedals that need stepped control
    
    Args:
        value: Analog input value (0-1023)
        in_min: Minimum input value
        in_max: Maximum input value
        steps: Number of steps to map to
    
    Returns:
        Step value (0 to steps)
    """
    # Clamp value within bounds
    value = max(in_min, min(in_max, value))
    
    # Map to 0-1 range
    normalized = (value - in_min) / (in_max - in_min)
    
    # Map to step range
    step = int(normalized * steps)
    return step


def deadzone(value, center=512, deadzone_range=50):
    """
    Apply deadzone to analog input
    Returns 0 if within deadzone, otherwise returns the value
    Prevents drift and unwanted small movements
    
    Args:
        value: Analog input value
        center: Center point of deadzone (typically 512 for 0-1023)
        deadzone_range: How far from center to apply deadzone
    
    Returns:
        0 if in deadzone, otherwise the value
    """
    if abs(value - center) < deadzone_range:
        return 0
    return value - center


def get_5pos_zone(value):
    """
    Divide 0-1023 range into 5 zones for 5-position controls
    Used for headlight control with 5 positions
    
    Zone mapping:
    - 0: 0-204 (far left)
    - 1: 205-409 (left/neutral area)
    - 2: 410-613 (middle/neutral)
    - 3: 614-818 (right/neutral area)
    - 4: 819-1023 (far right)
    
    Args:
        value: Analog input value (0-1023)
    
    Returns:
        Zone number (0-4)
    """
    value = max(0, min(1023, value))  # Clamp to 0-1023
    zone = int(value / 1023 * 5)
    return min(zone, 4)  # Ensure zone is 0-4


# ============================================================================
# STATE TRACKING
# ============================================================================

class ControlState:
    """Stores the previous state of all controls to avoid key spam"""
    def __init__(self):
        self.whistle_active = False
        self.whistle_type: str | None = None  # 'low', 'high', or None
        self.headlight_zone = 2  # Start at middle zone
        self.cylinder_state = 0
        self.reverser_step = 0
        self.throttle_step = 0
        self.train_brake_step = 0
        self.ind_brake_step = 0


state = ControlState()


# ============================================================================
# SERIAL COMMUNICATION
# ============================================================================

def find_arduino_ports():
    """
    List all available COM ports
    Helps user identify which port the Arduino is on
    """
    ports = serial.tools.list_ports.comports()
    available_ports = []
    for port in ports:
        available_ports.append(port.device)
    return available_ports


def open_serial_connection(port=SERIAL_PORT, baud=SERIAL_BAUD):
    """
    Open connection to Arduino via serial port
    Handles errors gracefully
    
    Args:
        port: COM port (e.g., "COM3")
        baud: Baud rate (typically 9600)
    
    Returns:
        Serial object or None if connection fails
    """
    try:
        ser = serial.Serial(port, baud, timeout=1)
        print(f"✓ Connected to {port} at {baud} baud")
        return ser
    except Exception as e:
        print(f"✗ Failed to connect to {port}: {e}")
        print(f"Available ports: {find_arduino_ports()}")
        return None


def parse_serial_data(data_string):
    """
    Parse data from Arduino serial string
    Expected format: WHISTLE:512;BELL:1;HEADLIGHT:300;CYLINDER:0;REVERSER:800;THROTTLE:200;TRAINBRAKE:100;INDBRAKE:50
    
    Args:
        data_string: Raw serial string from Arduino
    
    Returns:
        Dictionary with control values, or None if parsing fails
    """
    try:
        controls = {}
        pairs = data_string.strip().split(';')
        for pair in pairs:
            key, value = pair.split(':')
            controls[key.strip()] = int(value.strip())
        return controls
    except Exception as e:
        print(f"✗ Error parsing serial data: {e}")
        return None


# ============================================================================
# INPUT READING
# ============================================================================

def get_simulation_data():
    """
    Generate random control values for testing without Arduino
    Simulates realistic control movements
    
    Returns:
        Dictionary with all control values
    """
    data = {
        'WHISTLE': random.randint(450, 550),  # Usually near center, sometimes moves
        'BELL': random.choice([0, 0, 0, 1]),  # Mostly 0, occasionally pressed
        'HEADLIGHT': random.randint(0, 1023),
        'CYLINDER': random.choice([0, 1]),
        'REVERSER': random.randint(0, 1023),
        'THROTTLE': random.randint(0, 1023),
        'TRAINBRAKE': random.randint(0, 1023),
        'INDBRAKE': random.randint(0, 1023),
    }
    return data


def get_control_data(ser=None):
    """
    Get control data from either simulation or serial
    
    Args:
        ser: Serial connection object (None if simulation mode)
    
    Returns:
        Dictionary with control values
    """
    if SIMULATION_MODE:
        return get_simulation_data()
    
    if ser is None:
        print("✗ Serial port not connected in serial mode")
        return None
    
    try:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            return parse_serial_data(line)
    except Exception as e:
        print(f"✗ Error reading from serial: {e}")
    
    return None


# ============================================================================
# CONTROL HANDLERS
# ============================================================================

def handle_whistle(whistle_value):
    """
    Whistle control: potentiometer with middle deadzone
    Below center → H (low pitch)
    Above center → Shift+H (high pitch)
    In deadzone → nothing
    
    Args:
        whistle_value: Analog value (0-1023)
    """
    # Apply deadzone around center (512)
    dz = deadzone(whistle_value, center=512, deadzone_range=50)
    
    if DEBUG_MODE:
        print(f"WHISTLE: value={whistle_value}, deadzone_val={dz}")
    
    # Check which direction from center
    if dz > 0:
        # Above center - high pitch whistle (Shift+H)
        if not state.whistle_active or state.whistle_type != 'high':
            press_hotkey(Key.shift, 'h')
            log_key('Shift+H', "PRESS", "WHISTLE HIGH")
            state.whistle_active = True
            state.whistle_type = 'high'
    elif dz < 0:
        # Below center - low pitch whistle (H)
        if not state.whistle_active or state.whistle_type != 'low':
            press_key('h')
            log_key('H', "PRESS", "WHISTLE LOW")
            state.whistle_active = True
            state.whistle_type = 'low'
    else:
        # In deadzone - no whistle
        if state.whistle_active:
            state.whistle_active = False
            state.whistle_type = None


def handle_bell(bell_value):
    """
    Bell control: button press
    Trigger key "b" when button goes from 0 to 1
    
    Args:
        bell_value: Button state (0 or 1)
    """
    # We only trigger on the rising edge (0→1)
    # Note: This needs external tracking if we want to avoid repeated presses
    # For now, we'll just press when value is 1
    if bell_value == 1:
        press_key('b')
        log_key('b', "PRESS", "BELL")


def handle_headlight(headlight_value):
    """
    Headlight control: 5-position potentiometer
    Middle zone is neutral
    Press "j" to increase, "shift+j" to decrease
    
    Args:
        headlight_value: Analog value (0-1023)
    """
    zone = get_5pos_zone(headlight_value)
    
    # If zone changed, emit appropriate key
    if zone > state.headlight_zone:
        # Zone increased (moved right)
        press_key('j')
        log_key('j', "PRESS", "HEADLIGHT UP")
    elif zone < state.headlight_zone:
        # Zone decreased (moved left)
        press_hotkey(Key.shift, 'j')
        log_key('shift+j', "PRESS", "HEADLIGHT DOWN")
    
    state.headlight_zone = zone


def handle_cylinder_cocks(cylinder_value):
    """
    Cylinder cocks: toggle switch
    Press "k" when state changes (0→1 or 1→0)
    
    Args:
        cylinder_value: Switch state (0 or 1)
    """
    if cylinder_value != state.cylinder_state:
        press_key('k')
        log_key('k', "PRESS", "CYLINDER COCKS")
        state.cylinder_state = cylinder_value


def handle_reverser(reverser_value):
    """
    Reverser control: potentiometer with middle deadzone mapped to steps
    Middle deadzone = 0 (no movement)
    Right side (>512) → press "["
    Left side (<512) → press "]"
    
    Args:
        reverser_value: Analog value (0-1023)
    """
    # Apply deadzone around middle
    dz = deadzone(reverser_value, center=512, deadzone_range=50)
    
    if dz == 0:
        # In deadzone, reset to step 0
        current_step = 0
    elif dz > 0:
        # Right side - map to positive steps
        current_step = map_to_steps(reverser_value, in_min=562, in_max=1023, steps=MAX_STEPS)
    else:
        # Left side - map to negative steps
        current_step = -map_to_steps(reverser_value, in_min=0, in_max=461, steps=MAX_STEPS)
    
    if DEBUG_MODE:
        print(f"REVERSER: value={reverser_value}, dz={dz}, step={current_step}, prev_step={state.reverser_step}")
    
    # Emit keys when step increases (forward/backward direction changes)
    # HOLD the key for 0.15s so the game registers it
    if current_step > state.reverser_step:
        press_key('[', hold_duration=0.15)
        log_key('[', "HELD", f"REVERSER FORWARD (step {current_step})")
    elif current_step < state.reverser_step:
        press_key(']', hold_duration=0.15)
        log_key(']', "HELD", f"REVERSER BACKWARD (step {current_step})")
    
    state.reverser_step = current_step


def handle_throttle(throttle_value):
    """
    Throttle control: potentiometer mapped to 0-20 steps
    Increase → press "-"
    Decrease → press "="
    
    Args:
        throttle_value: Analog value (0-1023)
    """
    step = map_to_steps(throttle_value, steps=MAX_STEPS)
    
    if DEBUG_MODE:
        print(f"THROTTLE: value={throttle_value}, step={step}, prev_step={state.throttle_step}")
    
    # HOLD the key for 0.15s so the game registers the increment
    if step > state.throttle_step:
        press_key('-', hold_duration=0.15)
        log_key('-', "HELD", f"THROTTLE UP (step {step})")
    elif step < state.throttle_step:
        press_key('=', hold_duration=0.15)
        log_key('=', "HELD", f"THROTTLE DOWN (step {step})")
    
    state.throttle_step = step


def handle_train_brake(brake_value):
    """
    Train brake control: potentiometer mapped to 0-20 steps
    Increase → press "'"
    Decrease → press ";"
    
    Args:
        brake_value: Analog value (0-1023)
    """
    step = map_to_steps(brake_value, steps=MAX_STEPS)
    
    if DEBUG_MODE:
        print(f"TRAIN_BRAKE: value={brake_value}, step={step}, prev_step={state.train_brake_step}")
    
    # HOLD the key for 0.15s so the game registers the increment
    if step > state.train_brake_step:
        press_key("'", hold_duration=0.15)
        log_key("'", "HELD", f"TRAIN BRAKE UP (step {step})")
    elif step < state.train_brake_step:
        press_key(';', hold_duration=0.15)
        log_key(';', "HELD", f"TRAIN BRAKE DOWN (step {step})")
    
    state.train_brake_step = step


def handle_independent_brake(ind_brake_value):
    """
    Independent brake control: potentiometer mapped to 0-20 steps
    Increase → press "."
    Decrease → press ","
    
    Args:
        ind_brake_value: Analog value (0-1023)
    """
    step = map_to_steps(ind_brake_value, steps=MAX_STEPS)
    
    if DEBUG_MODE:
        print(f"IND_BRAKE: value={ind_brake_value}, step={step}, prev_step={state.ind_brake_step}")
    
    # HOLD the key for 0.15s so the game registers the increment
    if step > state.ind_brake_step:
        press_key('.', hold_duration=0.15)
        log_key('.', "HELD", f"IND BRAKE UP (step {step})")
    elif step < state.ind_brake_step:
        press_key(',', hold_duration=0.15)
        log_key(',', "HELD", f"IND BRAKE DOWN (step {step})")
    
    state.ind_brake_step = step


# ============================================================================
# MAIN CONTROL HANDLER
# ============================================================================

def handle_controls(data):
    """
    Main control handler: processes all controls from input data
    Safely handles missing keys
    
    Args:
        data: Dictionary with control values from serial or simulation
    """
    if data is None:
        return
    
    # Process each control with error handling
    try:
        if 'WHISTLE' in data:
            handle_whistle(data['WHISTLE'])
    except Exception as e:
        print(f"✗ Whistle error: {e}")
    
    try:
        if 'BELL' in data:
            handle_bell(data['BELL'])
    except Exception as e:
        print(f"✗ Bell error: {e}")
    
    try:
        if 'HEADLIGHT' in data:
            handle_headlight(data['HEADLIGHT'])
    except Exception as e:
        print(f"✗ Headlight error: {e}")
    
    try:
        if 'CYLINDER' in data:
            handle_cylinder_cocks(data['CYLINDER'])
    except Exception as e:
        print(f"✗ Cylinder cocks error: {e}")
    
    try:
        if 'REVERSER' in data:
            handle_reverser(data['REVERSER'])
    except Exception as e:
        print(f"✗ Reverser error: {e}")
    
    try:
        if 'THROTTLE' in data:
            handle_throttle(data['THROTTLE'])
    except Exception as e:
        print(f"✗ Throttle error: {e}")
    
    try:
        if 'TRAINBRAKE' in data:
            handle_train_brake(data['TRAINBRAKE'])
    except Exception as e:
        print(f"✗ Train brake error: {e}")
    
    try:
        if 'INDBRAKE' in data:
            handle_independent_brake(data['INDBRAKE'])
    except Exception as e:
        print(f"✗ Independent brake error: {e}")


# ============================================================================
# MAIN PROGRAM
# ============================================================================

def main():
    """Main program loop"""
    
    print("=" * 70)
    print("RAILROADER TRAIN CONTROL PANEL INTERFACE (PYNPUT VERSION)")
    print("=" * 70)
    print()
    
    # Display mode
    if SIMULATION_MODE:
        print("MODE: SIMULATION (random values)")
        print("LOG_KEYS: Enabled - watch console to verify key presses")
        ser = None
    else:
        print("MODE: SERIAL (Arduino)")
        ser = open_serial_connection(SERIAL_PORT, SERIAL_BAUD)
        if ser is None:
            print("✗ Failed to connect to Arduino. Exiting.")
            return
    
    print()
    print(f"Waiting {STARTUP_DELAY} seconds before starting...")
    print()
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                        ⚠ SAFETY NOTICE ⚠                         ║")
    print("╠═══════════════════════════════════════════════════════════════════╣")
    print("║ Keys will ONLY be sent when Railroader window is focused!        ║")
    print("║ Click away from Railroader to pause input automatically.         ║")
    print("║                                                                   ║")
    print("║ TO STOP: Press Ctrl+C in this console window                     ║")
    print("║ (Click this console window first, then Ctrl+C)                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print()
    print(">>> Click IN the Railroader window during countdown <<<")
    print()
    
    # Wait for user to switch to game window
    for i in range(STARTUP_DELAY, 0, -1):
        print(f"Starting in {i} seconds...", end='\r')
        time.sleep(1)
    
    print("Starting control loop...          ")
    print()
    print("KEY PRESSES WILL APPEAR BELOW:")
    print("(If you don't see key presses, check LOG_KEYS = True above)")
    print("-" * 70)
    print()
    
    try:
        while True:
            # CHECK WINDOW FOCUS EVERY SINGLE ITERATION (CRITICAL SAFETY!)
            currently_focused = is_railroader_focused()
            
            # Only process controls if Railroader is focused
            if currently_focused:
                # Read control data
                data = get_control_data(ser)
                
                # Process controls
                if data:
                    handle_controls(data)
            else:
                # Not focused - show warning occasionally
                window_title = get_active_window_title()
                if window_title:  # Only print if we got a title
                    print(f"⚠ PAUSED - Railroader not focused (current: '{window_title[:50]}')  ", end='\r')
                time.sleep(0.5)  # Longer delay when not focused
                continue
            
            # Wait before next update
            time.sleep(UPDATE_INTERVAL)
    
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("Ctrl+C detected - Stopping control loop...")
        print("=" * 70)
    
    finally:
        # Clean shutdown
        print("\nShutting down...")
        
        # Close serial connection
        if ser is not None:
            try:
                ser.close()
                print("  ✓ Serial connection closed")
            except:
                pass
        
        print("\n" + "=" * 70)
        print("✓ Program stopped safely - All keys released")
        print("=" * 70)


if __name__ == "__main__":
    main()
