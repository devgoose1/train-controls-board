"""
╔═══════════════════════════════════════════════════════════════════════╗
║                    SAFETY GUIDE - IMPORTANT!                          ║
╚═══════════════════════════════════════════════════════════════════════╝

The controller now has CRITICAL SAFETY FEATURES to prevent runaway input!

═══════════════════════════════════════════════════════════════════════

✓ WINDOW FOCUS DETECTION
────────────────────────────────────────────────────────────────────────
Keys are ONLY sent when Railroader window is focused.

If you click away from Railroader:
  → Input automatically PAUSES
  → Console shows: "Railroader NOT focused - Keys PAUSED"
  → Click back to Railroader to resume

This prevents keys from interfering with other programs!


✓ HOW TO STOP THE SCRIPT SAFELY
────────────────────────────────────────────────────────────────────────
METHOD 1 (Recommended):
  1. Click in the PowerShell/console window
  2. Press Ctrl+C
  3. Script stops immediately
  4. All held keys are released

METHOD 2 (If Ctrl+C doesn't work):
  1. Click away from Railroader (input pauses automatically)
  2. Alt+Tab to PowerShell window
  3. Press Ctrl+C or close the window

METHOD 3 (Emergency):
  1. Alt+Tab away from Railroader (keys stop)
  2. Open Task Manager (Ctrl+Shift+Esc)
  3. Find "Python" process
  4. End task


✓ TESTING THE SAFETY
────────────────────────────────────────────────────────────────────────
1. Run: python railroader_controller_pynput.py
2. During operation, click on your web browser or another window
3. Console should show: "Railroader NOT focused - Keys PAUSED"
4. Click back to Railroader
5. Console shows: "Railroader FOCUSED - Sending keys"

If this happens → SAFETY IS WORKING! ✓


✓ CUSTOMIZING WINDOW NAME
────────────────────────────────────────────────────────────────────────
If the script doesn't detect Railroader, edit this line in the script:

    WINDOW_NAME = "Railroader"  # Change if your window title differs

Check your exact window title:
  1. Open Railroader
  2. Look at the window title bar
  3. Use the exact text (case doesn't matter)


✓ WHAT HAPPENS WHEN SCRIPT STOPS
────────────────────────────────────────────────────────────────────────
When you press Ctrl+C:
  ✓ Whistle key ('v') is released (no stuck blowing!)
  ✓ Serial connection closes gracefully
  ✓ Console shows "Program stopped safely"
  ✓ All resources cleaned up


✓ BEST PRACTICES
────────────────────────────────────────────────────────────────────────
✓ Always keep PowerShell console visible (don't minimize)
✓ Test clicking away before full operation
✓ Use windowed mode in Railroader (easier to switch windows)
✓ Don't Alt+Tab rapidly while running (let focus detection catch up)
✓ If stuck, click away from Railroader first


✓ TROUBLESHOOTING
────────────────────────────────────────────────────────────────────────
Issue: "Keys still sending when I click away"
  → Window name detection failed
  → Check WINDOW_NAME matches your window title
  → Run this to see active window:
     
     python -c "import ctypes; hwnd = ctypes.windll.user32.GetForegroundWindow(); length = ctypes.windll.user32.GetWindowTextLengthW(hwnd); buff = ctypes.create_unicode_buffer(length + 1); ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1); print(f'Active window: {buff.value}')"

Issue: "Can't stop with Ctrl+C"
  → Click this console window first
  → Then try Ctrl+C again
  → Or close the console window entirely

Issue: "Whistle stuck on after stopping"
  → Manually press 'v' key to unstick
  → Script should auto-release, but manual backup works

Issue: "Lost control entirely"
  → Press Windows key (returns to desktop)
  → Alt+Tab to another window (pauses input)
  → Ctrl+Shift+Esc → End Python task


═══════════════════════════════════════════════════════════════════════

YOU ARE NOW PROTECTED! 🛡️

The script will NOT send keys unless Railroader is focused.
Press Ctrl+C anytime to stop safely.

═══════════════════════════════════════════════════════════════════════
"""

print(__doc__)
