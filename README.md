# Railroader Train Control Panel Interface

A Python application that reads control values from either simulation mode or Arduino hardware and translates them into keyboard commands for the game **Railroader**.

---

## QUICK START

### Step 1: Create Anaconda Environment

Open PowerShell and run:

```powershell
conda create -n train-driving python=3.11 -y
conda activate train-driving
```

You should see `(train-driving)` in your prompt.

### Step 2: Install Packages

```powershell
pip install pyautogui pyserial
```

### Step 3: Run the Application

```powershell
python railroader_controller.py
```

The program will:

1. Display the current mode (SIMULATION or SERIAL)
2. Show a 5-second countdown
3. Wait for you to switch to the Railroader game window
4. Start reading controls and sending keyboard commands

Press **Ctrl+C** to stop gracefully.

---

## HOW TO USE

### Running in Simulation Mode (Testing)

By default, the controller runs in **SIMULATION_MODE = True**, which generates random control values. This is perfect for:

- Testing the script without hardware
- Learning how the controls work
- Verifying Railroader is receiving key presses

Just run: `python railroader_controller.py`

### Switching to Arduino Mode

Edit the file `railroader_controller.py` and change:

```python
SIMULATION_MODE = True  # Change to False
```

to:

```python
SIMULATION_MODE = False
```

Also set the correct COM port:

```python
SERIAL_PORT = "COM3"  # Change to your Arduino's port
```

---

## HOW TO FIND THE CORRECT COM PORT

### On Windows

1. **Using Device Manager:**
   - Plug in your Arduino
   - Open **Device Manager** (Win + X, then device manager)
   - Look under "Ports (COM & LPT)"
   - Your Arduino should appear as "Arduino Uno" or similar
   - Note the COM number (e.g., COM3, COM4)

2. **Using Arduino IDE:**
   - Open Arduino IDE
   - Go to **Tools → Port**
   - Your Arduino's COM port will be listed there

3. **Using Python script:**
   - Run this Python code to list available ports:

   ```python
   import serial.tools.list_ports
   ports = serial.tools.list_ports.comports()
   for port in ports:
       print(port.device, "-", port.description)
   ```

4. **Common COM Ports:**
   - `COM3`, `COM4`, `COM5` are typical
   - Avoid `COM1` (usually reserved for system)

### Updating the Port in the Script

```python
SERIAL_PORT = "COM3"  # Change "COM3" to your actual port
SERIAL_BAUD = 9600   # Match your Arduino's baud rate (typically 9600)
```

---

## CONTROL MAPPINGS

| Control | Input | Behavior | Railroader Key |
| --------- | ------- | ---------- | --------------- |
| **WHISTLE** | Potentiometer | Hold when outside deadzone (±50 from 512) | `v` |
| **BELL** | Button | Press when button = 1 | `b` |
| **HEADLIGHT** | 5-Position Pot | Increase zone = next position, Decrease = previous | `j` / `shift+j` |
| **CYLINDER COCKS** | Toggle Switch | Press on state change | `k` |
| **REVERSER** | Potentiometer | Right = forward, Left = backward (±50 deadzone) | `[` / `]` |
| **THROTTLE** | Potentiometer | 0-1023 mapped to 0-20 steps | `-` / `=` |
| **TRAIN BRAKE** | Potentiometer | 0-1023 mapped to 0-20 steps | `'` / `;` |
| **INDEPENDENT BRAKE** | Potentiometer | 0-1023 mapped to 0-20 steps | `.` / `,` |

---

## SERIAL DATA FORMAT

When using Arduino mode, the controller expects data in this exact format:

```text
WHISTLE:512;BELL:1;HEADLIGHT:300;CYLINDER:0;REVERSER:800;THROTTLE:200;TRAINBRAKE:100;INDBRAKE:50
```

**Format explanation:**

- Each control name followed by colon and value
- Values separated by semicolons
- One line per update
- Analog values: 0-1023 (from ADC)
- Digital values: 0 or 1 (from digital pins)

**Example Arduino sketch:** See `arduino_example.ino` for reference implementation.

---

## CONFIGURATION

Edit these values in `railroader_controller.py`:

```python
SIMULATION_MODE = True           # True = random values, False = real Arduino
UPDATE_INTERVAL = 0.05           # Seconds between updates (lower = more responsive)
MAX_STEPS = 20                   # Steps for throttle/brake (0-20)
SERIAL_PORT = "COM3"             # Your Arduino's COM port
SERIAL_BAUD = 9600               # Must match Arduino sketch
STARTUP_DELAY = 5                # Seconds to switch to game before starting
```

**Recommendations:**

- `UPDATE_INTERVAL = 0.05` (50ms) is responsive but not too fast
- `MAX_STEPS = 20` gives fine control (many games use 20+ notches)
- Keep `STARTUP_DELAY = 5` to have time to switch windows

---

## TROUBLESHOOTING

### Issue: "ModuleNotFoundError: No module named 'pyautogui'"

**Solution:** You skipped Step 2. Run:

```powershell
pip install pyautogui pyserial
```

### Issue: "ERROR: Could not open COM port"

**Possible causes:**

1. Arduino not plugged in
2. Wrong COM port specified
3. COM port in use by another program

**Solutions:**

- Check Device Manager for correct COM port
- Unplug Arduino and plug back in
- Close Arduino IDE or other serial monitors
- Try: `python railroader_controller.py` with different COM ports

### Issue: "pyserial.serialutil.SerialException: The system cannot find the file specified"

**Solution:** Your Arduino is not connected or COM port is wrong.

- Run the COM port detection script above
- Update `SERIAL_PORT` in the script
- Check Arduino USB cable is working

### Issue: Keys not being sent to Railroader

**Possible causes:**

1. Railroader window not active when script starts
2. Pyautogui security block (some Windows versions)
3. Railroader is running but not focused

**Solutions:**

- Make sure Railroader window is active (in focus)
- Click in the Railroader window after the 5-second countdown
- Try running Python as Administrator (right-click → Run as Administrator)
- Disable Windows Defender/Antivirus momentarily to test

### Issue: Controls are too sensitive or jerky

**Solutions:**

- Increase `UPDATE_INTERVAL` to 0.1 (100ms)
- Add smoothing logic in Arduino sketch (averaging readings)
- Check potentiometer isn't noisy (bad electrical connection)

### Issue: No serial data is being read

**Solutions:**

1. Verify Arduino sketch is uploaded correctly
2. Test with Arduino Serial Monitor (Tools → Serial Monitor)
3. Check `SERIAL_BAUD` matches Arduino sketch (usually 9600)
4. Run: `python railroader_controller.py` in SIMULATION_MODE to test

### Issue: Deadzone not working for WHISTLE/REVERSER

This is normal. Deadzone prevents unwanted small movements. When you stop moving the control:

- **WHISTLE** should release the `v` key within deadzone
- **REVERSER** should not send keys when centered

If it's not working:

- Potentiometer might be worn out or drifting
- Increase `deadzone_range` (currently 50):

  ```python
  dz = deadzone(whistle_value, center=512, deadzone_range=100)  # Larger deadzone
  ```

### Issue: Multiple key presses for one control movement

**Why:** Key repeating is prevented by state tracking. You should only get one key press per step change.

**If still happening:**

- This is expected behavior for stepped controls
- The game may be repeating keys if not releasing them properly
- Try slightly increasing `UPDATE_INTERVAL`

---

## DEVELOPMENT & CUSTOMIZATION

### Modifying Key Mappings

Edit the `handle_*` functions in `railroader_controller.py`. For example, to change WHISTLE key:

```python
def handle_whistle(whistle_value):
    dz = deadzone(whistle_value, center=512, deadzone_range=50)
    is_active = dz != 0
    
    if is_active and not state.whistle_active:
        pyautogui.keyDown('v')  # Change 'v' to your key here
        state.whistle_active = True
    elif not is_active and state.whistle_active:
        pyautogui.keyUp('v')    # Change 'v' here too
        state.whistle_active = False
```

Available `pyautogui` keys: `'a'`, `'b'`, `'v'`, etc. For special keys, see [pyautogui docs](https://pyautogui.readthedocs.io/en/latest/keyboard.html#key-names).

### Adding New Controls

1. **Add to SERIAL_MODE format** in Arduino sketch (add new control value)
2. **Create new handler function:**

   ```python
   def handle_my_control(value):
       # Your logic here
       pyautogui.press('your_key')
   ```

3. **Call from `handle_controls()`:**

   ```python
   if 'MY_CONTROL' in data:
       handle_my_control(data['MY_CONTROL'])
   ```

### Adjusting Deadzone Values

| Control | Current Deadzone | Purpose |
| --------- | -------------------- | ----------------------------- |
| WHISTLE | ±50 from 512 | Prevents whistle while idle |
| REVERSER | ±50 from 512 | Prevents accidental forward/backward |

To adjust, modify the `deadzone()` function calls:

```python
dz = deadzone(value, center=512, deadzone_range=100)  # Larger deadzone
```

---

## TESTING CHECKLIST

- [ ] Anaconda environment created and activated (`(train-driving)` in prompt)
- [ ] `pip install pyautogui pyserial` completed
- [ ] Script runs in SIMULATION_MODE without errors
- [ ] Arduino connected and COM port identified
- [ ] Serial data format verified with Serial Monitor
- [ ] SERIAL_PORT set to correct COM in script
- [ ] Railroader launched and in focus
- [ ] Keys received in game with test inputs

---

## FILE STRUCTURE

```text
train-controls-board/
├── railroader_controller.py    # Main Python script (RUN THIS)
├── arduino_example.ino          # Arduino sketch example
└── README.md                   # This file
```

---

## PERFORMANCE NOTES

- **UPDATE_INTERVAL = 0.05** means controls update 20 times per second (perfectly responsive)
- Each control is independent, so one delay doesn't affect others
- Memory usage: Very low (~20MB)
- CPU usage: Minimal (CPU idle between updates)
- Tested on Windows 10/11 with Python 3.11

---

## SAFETY FEATURES

1. **Failsafe Disabled:** `pyautogui.FAILSAFE = False` allows continuous control
2. **Key Release:** Keys are properly released on exit (Ctrl+C)
3. **State Tracking:** Prevents key spam from repeated presses
4. **Error Handling:** Each control wrapped in try/except
5. **Graceful Shutdown:** Serial connection properly closed
6. **Deadzone Protection:** Prevents accidental inputs on idle controls

---

## REFERENCES

- [pyautogui Documentation](https://pyautogui.readthedocs.io/)
- [pyserial Documentation](https://pyserial.readthedocs.io/)
- [Arduino IDE](https://www.arduino.cc/en/software)
- [Railroader Game](https://www.railroadertycyclerailway.com/)

---

## VERSION

- **Version:** 1.0
- **Python:** 3.11+
- **Last Updated:** February 2026

---

## SUPPORT

If you encounter issues:

1. Check this troubleshooting section
2. Verify Arduino sketch is correct (see `arduino_example.ino`)
3. Test in SIMULATION_MODE first
4. Check COM port is correct
5. Run as Administrator if keys aren't being sent

For serial issues, open Arduino Serial Monitor and verify data is coming through.
