import pyautogui
import time
import random

pyautogui.FAILSAFE = False

# ==============================
# CONFIG
# ==============================

SIMULATION_MODE = True   # Zet op False wanneer je Arduino gebruikt
UPDATE_INTERVAL = 0.05   # 50ms

MAX_STEPS = 20           # Voor throttle & brakes

# ==============================
# STATE STORAGE
# ==============================

previous = {
    "whistle_active": False,
    "bell": 0,
    "cylinder": 0,
    "headlight_zone": 2,
    "reverser_zone": 0,
    "throttle_step": 0,
    "train_brake_step": 0,
    "ind_brake_step": 0,
}

# ==============================
# SIMULATIE DATA
# ==============================

def get_simulated_data():
    return {
        "WHISTLE": random.randint(0, 1023),
        "BELL": random.randint(0, 1),
        "HEADLIGHT": random.randint(0, 1023),
        "CYLINDER": random.randint(0, 1),
        "REVERSER": random.randint(0, 1023),
        "THROTTLE": random.randint(0, 1023),
        "TRAINBRAKE": random.randint(0, 1023),
        "INDBRAKE": random.randint(0, 1023),
    }

# ==============================
# HELPERS
# ==============================

def deadzone(value, center=512, zone=60):
    return abs(value - center) < zone

def map_to_steps(value, max_steps=MAX_STEPS):
    return int((value / 1023) * max_steps)

def get_5pos_zone(value):
    zone = int(value / 204.6)
    if zone > 4:
        zone = 4
    return zone

# ==============================
# CONTROL LOGIC
# ==============================

def handle_controls(data):
    global previous

    # ---------------- WHISTLE (v hold) ----------------
    if not deadzone(data["WHISTLE"]):
        if not previous["whistle_active"]:
            pyautogui.keyDown("v")
            previous["whistle_active"] = True
    else:
        if previous["whistle_active"]:
            pyautogui.keyUp("v")
            previous["whistle_active"] = False

    # ---------------- BELL (b) ----------------
    if data["BELL"] == 1 and previous["bell"] == 0:
        pyautogui.press("b")
    previous["bell"] = data["BELL"]

    # ---------------- CYLINDER COCKS (k) ----------------
    if data["CYLINDER"] != previous["cylinder"]:
        pyautogui.press("k")
        previous["cylinder"] = data["CYLINDER"]

    # ---------------- HEADLIGHT (5 standen) ----------------
    new_zone = get_5pos_zone(data["HEADLIGHT"])
    old_zone = previous["headlight_zone"]

    if new_zone != old_zone:
        diff = new_zone - old_zone
        if diff > 0:
            for _ in range(diff):
                pyautogui.press("j")
        else:
            for _ in range(abs(diff)):
                pyautogui.hotkey("shift", "j")

        previous["headlight_zone"] = new_zone

    # ---------------- REVERSER ----------------
    if deadzone(data["REVERSER"]):
        new_zone = 0
    elif data["REVERSER"] > 512:
        new_zone = map_to_steps(data["REVERSER"])
    else:
        new_zone = -map_to_steps(data["REVERSER"])

    old_zone = previous["reverser_zone"]

    if new_zone > old_zone:
        for _ in range(new_zone - old_zone):
            pyautogui.press("[")   # forward
    elif new_zone < old_zone:
        for _ in range(old_zone - new_zone):
            pyautogui.press("]")   # backward

    previous["reverser_zone"] = new_zone

    # ---------------- THROTTLE ----------------
    new_throttle = map_to_steps(data["THROTTLE"])
    old_throttle = previous["throttle_step"]

    if new_throttle > old_throttle:
        for _ in range(new_throttle - old_throttle):
            pyautogui.press("-")
    elif new_throttle < old_throttle:
        for _ in range(old_throttle - new_throttle):
            pyautogui.press("=")

    previous["throttle_step"] = new_throttle

    # ---------------- TRAIN BRAKE ----------------
    new_train = map_to_steps(data["TRAINBRAKE"])
    old_train = previous["train_brake_step"]

    if new_train > old_train:
        for _ in range(new_train - old_train):
            pyautogui.press("'")
    elif new_train < old_train:
        for _ in range(old_train - new_train):
            pyautogui.press(";")

    previous["train_brake_step"] = new_train

    # ---------------- INDEPENDENT BRAKE ----------------
    new_ind = map_to_steps(data["INDBRAKE"])
    old_ind = previous["ind_brake_step"]

    if new_ind > old_ind:
        for _ in range(new_ind - old_ind):
            pyautogui.press(".")
    elif new_ind < old_ind:
        for _ in range(old_ind - new_ind):
            pyautogui.press(",")

    previous["ind_brake_step"] = new_ind


# ==============================
# MAIN LOOP
# ==============================

print("Switch binnen 5 seconden naar Railroader!")
time.sleep(5)

while True:
    if SIMULATION_MODE:
        data = get_simulated_data()
    else:
        # Hier komt later serial uitlezing
        pass

    handle_controls(data)
    time.sleep(UPDATE_INTERVAL)
