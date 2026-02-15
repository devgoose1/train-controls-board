"""
TROUBLESHOOTING: Keys being sent but not working in Railroader
"""

print("""
╔════════════════════════════════════════════════════════════════════════╗
║             KEYS SENT BUT NOT WORKING IN RAILROADER                   ║
║                    TROUBLESHOOTING GUIDE                              ║
╚════════════════════════════════════════════════════════════════════════╝

STEP 1: Verify pyautogui is actually sending keys
────────────────────────────────────────────────────────────────────────

Run:
    python test_keys.py

This will:
- Send one key at a time
- Wait for you to observe the result
- Help identify if it's a Python problem or Railroader problem

Expected result:
- Lots of [CONTROL] PRESS: 'key' in your console
- Each key press should do something in Railroader

If keys aren't being seen:
   → Check that Railroader window is focused (title bar highlighted)
   → Windows security may be blocking: Try running as Administrator
   → Some games require specific focus methods


STEP 2: Check if it's a Railroader key binding issue
────────────────────────────────────────────────────────────────────────

In Railroader game settings, verify these key bindings exist:

   v         = WHISTLE
   b         = BELL
   j         = HEADLIGHT UP
   shift+j   = HEADLIGHT DOWN
   k         = CYLINDER COCKS
   [         = REVERSER FORWARD (or LEFT)
   ]         = REVERSER BACKWARD (or RIGHT)
   -         = THROTTLE UP
   =         = THROTTLE DOWN
   '         = TRAIN BRAKE UP
   ;         = TRAIN BRAKE DOWN
   .         = INDEPENDENT BRAKE UP
   ,         = INDEPENDENT BRAKE DOWN

If any of these aren't set, that control won't work!

To fix:
1. Open Railroader settings/options
2. Find "Controls" or "Key Bindings"
3. Check if each key above is mapped
4. If not, add the key binding
5. Test with test_keys.py again


STEP 3: Window Focus / Fullscreen Mode
────────────────────────────────────────────────────────────────────────

Some games (especially fullscreen exclusive mode) don't accept pyautogui input.

Try these:
✓ Run Railroader in WINDOWED MODE (not fullscreen)
✓ Run Python as ADMINISTRATOR (right-click PowerShell → Run as admin)
✓ Disable fullscreen exclusive mode in game settings
✓ Try borderless windowed mode if available

The key is: Game window must accept keyboard input from external sources.


STEP 4: Debug with logging enabled
────────────────────────────────────────────────────────────────────────

Edit railroader_controller.py and set:

    LOG_KEYS = True              # Show all key presses
    DEBUG_MODE = True            # Show values being read

Then run:
    python railroader_controller.py

Watch the console for output like:
    [WHISTLE] KEYDOWN: 'v'
    [THROTTLE (step 5)] PRESS: '-'

If you see these but nothing in game:
   → Railroader is not accepting pyautogui input
   → See "Window Focus" section above


STEP 5: Test with keyboard directly
────────────────────────────────────────────────────────────────────────

1. Keep railroader_controller.py running
2. While it's running, press one of these real keys on your keyboard
3. See if the game responds
4. If real keyboard works but controller doesn't:
   → pyautogui is blocked (see Step 3)
   → Run as Administrator or try windowed mode


ADVANCED: Check Windows Security Policies
────────────────────────────────────────────────────────────────────────

On some Windows systems, security prevents non-interactive input:

Try:
1. Right-click Python (pythonw.exe) → Properties → Compatibility
2. Check "Run as administrator"
3. Check "Reduced color mode"
4. Check "Run in fullscreen"
5. Apply → OK

OR: Run the script directly with admin:
   
    powershell -Command "Start-Process python -ArgumentList 'railroader_controller.py' -Verb RunAs"


STEP 6: Alternative: Using keyboard simulation (if all else fails)
────────────────────────────────────────────────────────────────────────

If pyautogui doesn't work, you can try pynput or keyboard library:

pip install pynput

Then modify the script to use pynput instead of pyautogui.
We can help with this if needed.


SYMPTOMS AND SOLUTIONS
════════════════════════════════════════════════════════════════════════

Issue: "Simulation runs but nothing in game"
Solution:
   1. Is Railroader window focused? (Check title bar highlight)
   2. Run: python diagnostics.py (check if pyautogui works)
   3. Run: python test_keys.py (send single keys and watch)
   4. Run as Administrator if not already

Issue: "Some keys work, others don't"
Solution:
   1. Check Railroader key bindings - a key might not be mapped
   2. Some keys might be system reserved (Windows key, Alt, etc)
   3. Try different keys: e.g., instead of "'" try "p"
   4. Edit railroader_controller.py to map different keys

Issue: "Works sometimes, not always"
Solution:
   1. Window focus issue - Railroader must stay focused
   2. Add delays between keys: increase UPDATE_INTERVAL = 0.1
   3. Check if Railroader has input lag or buffering

Issue: "Cannot get window to stay focused"
Solution:
   1. Place Railroader window in front before starting script
   2. Don't click mouse while script is running
   3. Some games steal focus - not much we can do from Python
   4. Try running windowed instead of fullscreen


QUICK TEST CHECKLIST
════════════════════════════════════════════════════════════════════════

☐ Railroader is running
☐ Railroader window is visible on screen
☐ Railroader has focus (title bar highlighted)
☐ Railroader key bindings are set (check in game options)
☐ Python script running in foreground (can see console)
☐ Waiting through 5-second countdown
☐ Clicked in Railroader window during countdown
☐ Not moving mouse while script runs
☐ Not clicking elsewhere during script runtime


IF NOTHING WORKS
════════════════════════════════════════════════════════════════════════

1. Post the OUTPUT from:
   - python diagnostics.py
   - python test_keys.py
   
2. Include these details:
   - Railroader game mode (ORTS? TSW? Other?)
   - Windows version
   - Python version (python --version)
   - Are you running in fullscreen or windowed?
   - Are you running as Administrator?
   - Have you checked key bindings in game?

3. We can provide advanced solutions like:
   - Using different key libraries (pynput, keyboard)
   - Custom window focusing code
   - Direct input methods
   - Serial/hardware controller workarounds


══════════════════════════════════════════════════════════════════════════
Need help? Check README.md for complete documentation
═══════════════════════════════════════════════════════════════════════════
""")
