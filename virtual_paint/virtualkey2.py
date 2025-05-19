import cv2
import numpy as np
import mediapipe as mp
import time
import math

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Extended keyboard layout
keyboard_layout = [
    ["~", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Back"],
    ["Shift", "Space", "Quit"]
]

shift_symbols = {
    '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
    '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
    '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|',
    ';': ':', "'": '"', ',': '<', '.': '>', '/': '?', '`': '~'
}

typed_text = ""
shift_on = False
last_click_time = 0

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Get actual resolution
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("Camera resolution:", frame_width, "x", frame_height)

# UI Config (based on frame width)
KEY_WIDTH = int(frame_width * 0.06)
KEY_HEIGHT = int(frame_height * 0.09)
KEY_SPACING = int(KEY_WIDTH * 0.2)
START_X = int(frame_width * 0.03)
START_Y = int(frame_height * 0.3)
MAX_ROW_WIDTH = frame_width - 2 * START_X

def draw_keyboard(img, layout, shift):
    key_list = []
    x = START_X
    y = START_Y

    for row in layout:
        for key in row:
            label = key
            w = KEY_WIDTH
            h = KEY_HEIGHT

            # Shift functionality
            if shift:
                if key.isalpha():
                    label = key.upper()
                elif key in shift_symbols:
                    label = shift_symbols[key]
            else:
                if key.isalpha():
                    label = key.lower()

            # Wide keys
            if key == "Space":
                w *= 5
            elif key in ["Shift", "Back", "Enter"]:
                w *= 2

            # Wrap if needed
            if x + w > MAX_ROW_WIDTH:
                x = START_X
                y += h + KEY_SPACING

            # Draw key
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 120, 200), -1)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 3)
            font_scale = w / 125.0
            cv2.putText(img, label, (x + 15, y + int(h * 0.7)), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 2)

            key_list.append((key, label, (x, y, x + w, y + h)))
            x += w + KEY_SPACING

        x = START_X
        y += h + KEY_SPACING

    return key_list

def draw_textbox(img, text):
    box_width = frame_width - 2 * START_X
    cv2.rectangle(img, (START_X, 50), (START_X + box_width, 120), (30, 30, 30), -1)
    font_scale = frame_width / 900.0
    cv2.putText(img, text, (START_X + 20, 100), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 3)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    key_boxes = draw_keyboard(img, keyboard_layout, shift_on)
    draw_textbox(img, typed_text)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = img.shape
            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]
            cx, cy = int(index_tip.x * w), int(index_tip.y * h)
            tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)

            # Draw fingertip
            cv2.circle(img, (cx, cy), 12, (0, 255, 255), -1)

            # Click detection
            distance = math.hypot(tx - cx, ty - cy)
            if distance < 50:
                current_time = time.time()
                if current_time - last_click_time > 0.8:
                    for key, label, (x1, y1, x2, y2) in key_boxes:
                        if x1 < cx < x2 and y1 < cy < y2:
                            if key == "Space":
                                typed_text += " "
                            elif key == "Back":
                                typed_text = typed_text[:-1]
                            elif key == "Enter":
                                typed_text += "\n"
                            elif key == "Shift":
                                shift_on = not shift_on
                            elif key == "Quit":
                                cap.release()
                                cv2.destroyAllWindows()
                                exit()
                            else:
                                typed_text += label
                            last_click_time = current_time
                            break

    cv2.imshow("Virtual Keyboard - Hand Gesture", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
