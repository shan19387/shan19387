import argparse, json, os, sys, threading, time
from pathlib import Path
from collections import deque

import cv2
import numpy as np
from pynput import mouse
from pynput import keyboard as pk
import pyautogui as pag

# -------------------
# Config
# -------------------
OUT_DIR = Path("data/frames")
OUT_DIR.mkdir(parents=True, exist_ok=True)
META_PATH = OUT_DIR / "meta.json"

MONITOR_INDEX = 1
CAPTURE_REGION = None  # None -> full monitor by MONITOR_INDEX

MIN_INTERVAL_MOVE_SEC = 0.08
MIN_MOVE_PIXELS = 20
LABEL_DEBOUNCE_SEC = 0.25
MAX_QUEUE = 2000
META_FLUSH_INTERVAL = 2.0  # seconds

MOVE = "MOVE"
LBTN_DOWN = "LBTN_DOWN"
LBTN_UP   = "LBTN_UP"
RBTN_DOWN = "RBTN_DOWN"
RBTN_UP   = "RBTN_UP"
MBTN_DOWN = "MBTN_DOWN"
MBTN_UP   = "MBTN_UP"
WHEEL     = "WHEEL"

pag.FAILSAFE = True
pag.PAUSE = 0.02

stop_flag = threading.Event()

def warn_if_wayland():
    if os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland":
        print("[WARN] Wayland detected. Global listeners/screenshots can be unreliable. Prefer Xorg.", file=sys.stderr)

def action_click_on_python_file():
    try:
        time.sleep(0.5)
        pag.click(781, 95)
        time.sleep(1.2)
        pag.click(71, 737)
        time.sleep(1.2)
        pag.press("enter")
    except pag.FailSafeException:
        print("[ABORT] PyAutoGUI failsafe triggered (moved mouse to a corner).")
    except Exception as e:
        print(f"[ERROR] CLICK_ON_PYTHON_FILE action failed: {e}")
def action_click_collect_data_python_file():
    try:
        time.sleep(1.2)
        pag.click(621, 74)
        time.sleep(1.2)
        pag.click(71, 737)
        time.sleep(1.2)
        pag.press("enter")
    except pag.FailSafeException:
        print("[ABORT] PyAutoGUI failsafe triggered (moved mouse to a corner).")
    except Exception as e:
        print(f"[ERROR] CLICK_CREATE_DATA_PYTHON_FILE action failed: {e}")
def action_code_in_math_python_file():
    try:
        time.sleep(1.2)
        pag.click(1023, 129)
        time.sleep(1.2)
        pag.typewrite("a = int(input('Enter first number: '))", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("b = int(input('Enter second number: '))", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("print('Sum: ', a + b) # The comma was added here instead of the plus sign", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# The reason why is because the plus sign is used in addition", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Therefore, had the print function been print('Sum: ' + a + b), you would get an error", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Therefore, it would make more sense for the comma to be placed in front of the last quotation mark displayed before the text", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# This goes for the difference, product, quotient, floor division, and remainder functions as well.", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("print('Difference: ', a - b)", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("print('Product: ', a * b)", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("print('Quotient: ', a / b)", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("print('Floor Division: ', a // b)", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("print('Remainder: ', a % b)", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# When dealing with numbers,...", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("#.... you must put the comma after 'Sum: ' or anything else math related", interval=0.05)
        time.sleep(0.5)
        pag.click(71, 737) # Clicks at the very coordinates where the terminal is
        time.sleep(1.2)
        pag.press("enter") # This initiates the input to show up once more
    except pag.FailSafeException:
        print("[ABORT] PyAutoGUI failsafe triggered (moved mouse to a corner).")
    except Exception as e:
        print(f"[ERROR] CODE_IN_MATH_PYTHON_FILE action failed: {e}")
def action_explain_in_math_python_file():
    try:
        time.sleep(1.2)
        pag.click(1023, 129)
        time.sleep(1.2)
        time.sleep(1)
        pag.typewrite("# For this assignment, you need inputs", interval=0.02)
        time.sleep(0.2)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# And not normal inputs, you need int inputs because when you are dealing with numbers, you might need to convert the normal input into an integer input", interval=0.02)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Here is the output that you are supposed to get", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Now here's the idea", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Sum: +, Difference: -, Product: *, Quotient: /, Floor Division: //, and Remainder: %", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Output(example):", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Enter first number: 8", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Enter second number: 2", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Sum: 10", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Difference: 6", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Product: 16", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Quotient: 4.0", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Floor Division: 4", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Remainder: 0", interval=0.05)
        pag.press("enter")
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Inputs", interval=0.05)
        pag.press("enter")
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Here is some code to give you an idea on how to start this", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("a = int(input('Enter first number: '))", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# a is the variable that represents the first number to be included. Whether or not you make a represent the first number that the user enters is up to you", interval=0.02)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Me personally, I use a as the letter variable that represents the first number because it is the first letter in the alphabet(alpha meaning beginning)", interval=0.02)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Now you might be asking 'Why does a = int(input('Enter first number: ')) have to be the function required for the input function?'", interval=0.02)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# The reason why a = int(input('Enter first number: ')) has to be used is because we are dealing with numbers in this case", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# This applies to the letter variable name that could represent the second number as well", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# If a = input('Enter first number: ') was used instead, you might get an error", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# This is why we want to stick with a = int(input('Enter first number: ')) in order to avoid getting any errors", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Now how do we get the output? We use the print function", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Well the correct answer is print('Sum: ' + a + b) right?", interval=0.05)
        pag.press("enter")
        time.sleep(2)
        pag.typewrite("# Actually, there are problems with making print('Sum: ' + a + b) as the print function.", interval=0.05)
        pag.press("enter")
        time.sleep(0.2)
        pag.typewrite("# Would it work for when the print function is print('Difference: ' + a - b)?", interval=0.05)
        pag.press("enter")
        time.sleep(0.2)
        pag.typewrite("# Actually, it seems that print('Difference: ' + a - b) might not be able to print the output that this file is supposed to print out", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# However, even if print('Difference: ' + a - b) printed the correct output for the difference between the first and second number,...", interval=0.02)
        time.sleep(1)
        pag.press("enter")
        time.sleep(1)
        pag.typewrite("#.... it won't work for Sum because the sum of two numbers is when 2 numbers are added together", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# So what if instead of applying the plus sign right after 'Sum: ', 'Difference: ', 'Product: ', 'Quotient: ', 'Floor Division: ', and 'Remainder: ',....", interval=0.02)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("#.... we add a comma after 'Sum: ', 'Difference: ', 'Product: ', 'Quotient: ', 'Floor Division: ', and 'Remainder: ' instead?", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# The reason why this works is because it allows the print function to print out the exact output that the project requires", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# So feel free to do the following steps with your code before you attempt at trying to meet the output requirements for your assignment: ", interval=0.02)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Step 1: Type the following code in between the Step 1 and Step 2 comments: ", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# print('Sum: ', a + b)", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Step 2: Run the code using whatever means necessary, whether you have to run it through virtual environment or whether you don't.", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# If you're using Pycharm, you may have to run the program in a different way than what is being demonstrated in Visual Studio Code.", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# If you get the following output: ", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Enter first number: 8", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Enter second number: 2", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Sum: 10", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Then this means that the code that you have entered is correct.", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# If this output doesn't show up, it means you need to fix something about the code.", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# After you get the correct output for sum, apply the comma after the parentheses within the print function for difference, product, quotient, floor division, and remainder of the two numbers next.", interval=0.05)
        pag.press("enter")
        time.sleep(0.5)
        pag.typewrite("# Please refer to the very top of the python file for reference to the final output and the addition, subtraction, multiplication, division, floor division, and remainder signs.", interval=0.02)
        time.sleep(1.2)
        pag.click(71, 737)
        time.sleep(1.2)
        pag.press("enter")
    except pag.FailSafeException:
        print("[ABORT] PyAutoGUI failsafe triggered (moved mouse to a corner).")
    except Exception as e:
        print(f"[ERROR] EXPLAIN_IN_MATH_PYTHON_FILE action failed: {e}")
def action_select_all_text():
    try:
        time.sleep(1.2)
        pag.click(1023, 129)
        pag.hotkey("ctrl", "a")
        time.sleep(1.2)
        pag.click(71, 737)
        time.sleep(1.2)
        pag.press("enter")
    except pag.FailSafeException:
        print("[ABORT] PyAutoGUI failsafe triggered (moved mouse to a corner).")
    except Exception as e:
        print(f"[ERROR] SELECT_ALL_TEXT action failed: {e}")
def action_delete():
    try:
        time.sleep(1.2)
        pag.click(1023,129)
        time.sleep(1.2)
        pag.hotkey("ctrl", "a")
        time.sleep(1.2)
        pag.press("delete")
        time.sleep(1.2)
        pag.click(71, 737)
        time.sleep(1.2)
        pag.press("enter")
    except pag.FailSafeException:
        print("[ABORT] PyAutoGUI failsafe triggered (moved mouse to a corner).")
    except Exception as e:
        print(f"[ERROR] DELETE action failed: {e}")
def action_copy():
    try:
        time.sleep(1.2)
        pag.click(1023, 129)
        time.sleep(1.2)
        pag.hotkey("ctrl", "a")
        time.sleep(1.2)
        pag.hotkey("ctrl", "c")
        time.sleep(1.2)
        pag.click(71, 737)
        time.sleep(1.2)
        pag.press("enter")
    except pag.FailSafeException:
        print("[ABORT] PyAutoGUI failsafe triggered (moved mouse to a corner).")
    except Exception as e:
        print(f"[ERROR] COPY action failed: {e}")
def action_paste():
    try:
        time.sleep(1.2)
        pag.click(1023, 129)
        time.sleep(1.2)
        pag.hotkey("ctrl", "v")
        time.sleep(1.2)
        pag.click(71, 737)
        time.sleep(1.2)
        pag.press("enter")
    except pag.FailSafeException:
        print("[ABORT] PyAutoGUI failsafe triggered (moved mouse to a corner).")
    except Exception as e:
        print(f"[ERROR] PASTE action failed: {e}")
def action_windows_menu():
    try:
        pag.press("winleft")
    except pag.FailSafeException:
        print("[ABORT] PyAutoGUI failsafe triggered (moved mouse to a corner).")
    except Exception as e:
        print(f"[ERROR] WINDOWS_MENU action failed: {e}")
def action_type_firefox_enter():
    try:
        pag.typewrite("Firefox", interval=0.05)
        pag.press("enter")
    except pag.FailSafeException:
        print("[ABORT] PyAutoGUI failsafe triggered (moved mouse to a corner).")
    except Exception as e:
        print(f"[ERROR] TYPE_FIREFOX_ENTER action failed: {e}")
def action_enter_website_address():
    try:
        pag.hotkey("ctrl", "l")
    except pag.FailSafeException:
        print("[ABORT] PyAutoGUI failsafe triggered (moved mouse to a corner).")
    except Exception as e:
        print(f"[ERROR] ENTER_WEBSITE_ADDRESS action failed: {e}")
def action_type_google_enter():
    try:
        pag.typewrite("google.com", interval=0.05)
        pag.press("enter")
    except pag.FailSafeException:
        print("[ABORT] PyAutoGUI failsafe triggered (moved mouse to a corner).")
    except Exception as e:
        print(f"[ERROR] TYPE_GOOGLE.COM_ENTER action failed: {e}")


LABEL_ACTIONS = {
    "IDLE": lambda: None,
    "CLICK_ON_PYTHON_FILE": action_click_on_python_file,
    "CLICK_CREATE_DATA_PYTHON_FILE": action_click_collect_data_python_file,
    "CODE_IN_MATH_PYTHON_FILE": action_code_in_math_python_file,
    "EXPLAIN_IN_MATH_PYTHON_FILE": action_explain_in_math_python_file,
    "SELECT_ALL_TEXT": action_select_all_text,
    "DELETE": action_delete,
    "COPY": action_copy,
    "PASTE": action_paste,
    "WINDOWS_MENU": action_windows_menu,
    "TYPE_FIREFOX_ENTER": action_type_firefox_enter,
    "ENTER_WEBSITE_ADDRESS": action_enter_website_address,
    "TYPE_GOOGLE.COM_ENTER": action_type_google_enter,
}
def perform_action(label_name: str):
    fn = LABEL_ACTIONS.get(label_name)
    if not fn:
        print(f"[WARN] No action defined for label '{label_name}'")
        return
    fn()

# -------------------
# Helpers
# -------------------
def euc_dist(a, b): 
    dx = a[0] - b[0]; dy = a[1] - b[1]
    return (dx*dx + dy*dy) ** 0.5 # This could possibly be the math needed for determing the mechanics of a moving mouse

def cli_prompt_loop(event_queue, stop_flag):
    choices = ", ".join(LABEL_ACTIONS.keys())
    while not stop_flag.is_set():
        try:
            lbl = input(f"Enter label (choices: {choices}; 'exit' to quit): ").strip()
        except EOFError:
            break  # stdin closed

        if not lbl:
            continue
        if lbl.lower() in ("exit", "quit"):
            stop_flag.set()
            break
        if lbl not in LABEL_ACTIONS:
            print(f"[WARN] Unknown label '{lbl}'.")
            continue

        # enqueue one-time key event
        event_queue.append(("key", lbl, None, None, None))
        print(f"[ENQUEUE] {lbl}")

def start_capture(label_to_run: str | None):
    from mss import mss

    lock = threading.Lock()
    event_queue = deque(maxlen=MAX_QUEUE)

    meta = {
        "monitor_index": MONITOR_INDEX,
        "region": CAPTURE_REGION,
        "frames": []
    }

    last_move_time = 0.0 # This is the initial last time the mouse moved, which is set to none unless the mouse moves
    last_move_pos = None # This is the last position the mouse is in, which in this case, it hasn't moved to a position yet
    last_label_time = {name: 0.0 for name in LABEL_ACTIONS.keys()}
    last_meta_flush = time.time()

    # -------------------
    # Start CLI prompt loop here
    # -------------------
    prompt_thread = threading.Thread(
        target=cli_prompt_loop, args=(event_queue, stop_flag), daemon=True
    )
    prompt_thread.start()
    

    def on_move(x, y):
        nonlocal last_move_time, last_move_pos
        now = time.time()
        if (now - last_move_time) < MIN_INTERVAL_MOVE_SEC:
            return
        if last_move_pos is not None and euc_dist((x, y), last_move_pos) < MIN_MOVE_PIXELS:
            return
        last_move_time = now
        last_move_pos = (x, y)
        event_queue.append(("mouse", MOVE, x, y, None))

    def on_click(x, y, button, pressed):
        if button == mouse.Button.left:
            name = LBTN_DOWN if pressed else LBTN_UP
        elif button == mouse.Button.right:
            name = RBTN_DOWN if pressed else RBTN_UP
        elif button == mouse.Button.middle:
            name = MBTN_DOWN if pressed else MBTN_UP
        else:
            name = f"BTN_{button}_{'DOWN' if pressed else 'UP'}"
        event_queue.append(("mouse", name, x, y, None))

    def on_scroll(x, y, dx, dy):
        event_queue.append(("mouse", WHEEL, x, y, int(dy)))

    def on_press(key):
        # ESC to stop
        if key == pk.Key.esc:
            stop_flag.set()
            return

        # Optional: map single-character keys to LABEL names if you later want hotkeys
        # e.g., press 'm' to enqueue "TYPE_MATH_PYTHON_FILE"
        try:
            ch = key.char  # raises for non-char keys
        except Exception:
            return
        # Example hotkey mapping (customize or remove)
        hotkey_map = {pk.Key.f10: "CLICK_ON_PYTHON_FILE",
                      pk.Key.f9: "CLICK_CREATE_DATA_PYTHON_FILE",
                      pk.Key.f8: "CODE_IN_MATH_PYTHON_FILE",
                      pk.Key.f7: "EXPLAIN_IN_MATH_PYTHON_FILE",
                      pk.Key.f6: "SELECT_ALL_TEXT",
                      pk.Key.f5: "DELETE",
                      pk.Key.f4: "COPY",
                      pk.Key.f3: "PASTE",
                      pk.Key.f2: "WINDOWS_MENU",
                      pk.Key.f1: "TYPE_FIREFOX_ENTER"}
        lbl = hotkey_map.get(ch)
        if not lbl:
            return
        now = time.time()
        if (now - last_label_time.get(lbl, 0.0)) >= LABEL_DEBOUNCE_SEC:
            event_queue.append(("key", lbl, None, None, None))
            last_label_time[lbl] = now

    k_listener = pk.Listener(on_press=on_press)
    k_listener.start()

    m_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    m_listener.start()

    def region_for_mss(sct):
        try:
            if CAPTURE_REGION is not None:
                return {
                    "left": int(CAPTURE_REGION["left"]),
                    "top": int(CAPTURE_REGION["top"]),
                    "width": int(CAPTURE_REGION["width"]),
                    "height": int(CAPTURE_REGION["height"]),
                }
            return sct.monitors[MONITOR_INDEX] if MONITOR_INDEX < len(sct.monitors) else sct.monitors[0]
        except Exception as e:
            print(f"[WARN] region_for_mss fallback to all monitors: {e}")
            return sct.monitors[0]

    def worker():
        nonlocal last_meta_flush
        counter = 0
        with mss() as sct:
            reg = region_for_mss(sct)
            while not stop_flag.is_set():
                try:
                    etype, name, x, y, wheel = event_queue.popleft()
                except IndexError:
                    time.sleep(0.005)
                    # periodic meta flush
                    if time.time() - last_meta_flush >= META_FLUSH_INTERVAL:
                        with lock:
                            with open(META_PATH, "w") as f:
                                json.dump(meta, f, indent=2)
                        last_meta_flush = time.time()

                    # heartbeat (optional)
                    idle_interval=3.0
                    if time.time() - last_meta_flush >= idle_interval:
                        ts_ms = int(time.time() * 1000)
                        shot = sct.grab(reg)
                        frame = np.array(shot)[:, :, :3]
                        fname = f"{ts_ms}_idle_heartbeat.jpg"
                        cv2.imwrite(str(OUT_DIR / fname), frame)
                        with lock:
                            meta["frames"].append({"file": fname, "type": "idle", "name": "HEARTBEAT", "t": ts_ms})
                        last_meta_flush = time.time()
                    continue

                # 1) snapshot first
                ts_ms = int(time.time() * 1000)
                shot = sct.grab(reg)
                frame = np.array(shot)[:, :, :3]
                if etype == "mouse":
                    fname = f"{ts_ms}_{etype}_{name}_{int(x or 0)}_{int(y or 0)}_{counter:06d}.jpg"
                else:
                    fname = f"{ts_ms}_{etype}_{name}_{counter:06d}.jpg"

                cv2.imwrite(str(OUT_DIR / fname), frame)

                rec = {"file": fname, "type": etype, "name": name, "t": ts_ms}
                if x is not None and y is not None:
                    rec["x"], rec["y"] = int(x), int(y)
                if wheel is not None:
                    rec["wheel"] = int(wheel)

                with lock:
                    meta["frames"].append(rec)

                # logging
                if etype == "mouse":
                    if x is not None and y is not None:
                        print(f"[{name:10s}] ({int(x):4d},{int(y):4d}) -> {fname}")
                    else:
                        print(f"[{name:10s}] -> {fname}")
                else:
                    print(f"[KEY {name}] -> {fname}")

                # 2) perform action AFTER snapshot (for key events)
                if etype == "key":
                    try:
                        perform_action(name)
                    except Exception as e:
                        print(f"[ERROR] Action '{name}' failed: {e}")

                counter += 1

    t = threading.Thread(target=worker, daemon=True)
    t.start()

    # if user passed a label to run once at start, enqueue it as a key event
    if label_to_run:
       print(f"[BOOT] enqueue: {label_to_run}")
       event_queue.append(("key", label_to_run, None, None, None))



    try:
        while not stop_flag.is_set():
            time.sleep(0.02)
    except KeyboardInterrupt:
        pass
    finally:
        stop_flag.set()
        try:
            m_listener.stop(); m_listener.join(timeout=1.0)
        except Exception:
            pass
        try:
            k_listener.stop(); k_listener.join(timeout=1.0)
        except Exception:
            pass
        try:
            t.join(timeout=1.0)
        except Exception:
            pass
        with open(META_PATH, "w") as f:
            json.dump(meta, f, indent=2)
        print(f"\nSaved {len(meta['frames'])} frames + meta to: {META_PATH}")

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["capture", "action"], default="capture",
                   help="capture = passive capture; action = run a label action (and capture)")
    p.add_argument("--label", default=None, help="Label name to run in action mode")
    return p.parse_args()

def main():
    warn_if_wayland()
    args = parse_args()

    # Always prompt if no label provided
    if not args.label:
        choices = ", ".join(LABEL_ACTIONS.keys())
        args.label = input(f"Enter label (e.g., {choices}): ").strip() or "IDLE"

    # If a label is present, run as 'action' so it's enqueued at startup
    args.mode = "action"

    print(f"Running in mode={args.mode}, label={args.label}")

    start_capture(args.label)



if __name__ == "__main__":
    main()