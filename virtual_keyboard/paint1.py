import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Webcam and canvas setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
canvas = np.zeros((720, 1280, 3), np.uint8)

# Button configuration
buttons = [
    {"label": "Free Draw", "pos": (20, 20), "mode": "free"},
    {"label": "Line", "pos": (150, 20), "mode": "line"},
    {"label": "Rectangle", "pos": (260, 20), "mode": "rectangle"},
    {"label": "Eraser", "pos": (400, 20), "mode": "erase"},
    {"label": "Clear", "pos": (510, 20), "mode": "clear"},
    {"label": "Red", "pos": (630, 20), "mode": "color_red"},
    {"label": "Black", "pos": (740, 20), "mode": "color_black"},
    {"label": "Quit", "pos": (850, 20), "mode": "quit"}
]

# Variables
selected_mode = None
draw_mode = None
start_point = None
prev_point = None
color = (0, 0, 255)  # Default color: red

# Fingertip landmarks
tip_ids = [4, 8, 12, 16, 20]

def count_fingers(lm_list):
    fingers = []
    if lm_list[tip_ids[0]][0] > lm_list[tip_ids[0] - 1][0]:
        fingers.append(1)
    else:
        fingers.append(0)
    for i in range(1, 5):
        if lm_list[tip_ids[i]][1] < lm_list[tip_ids[i] - 2][1]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

def draw_buttons(img, selected_mode):
    for btn in buttons:
        x, y = btn["pos"]
        w, h = 100, 40
        is_selected = (btn["mode"] == selected_mode) or \
                      (btn["mode"] == "color_red" and color == (0, 0, 255)) or \
                      (btn["mode"] == "color_black" and color == (0, 0, 0))
        box_color = (0, 255, 0) if is_selected else (255, 0, 0)
        cv2.rectangle(img, (x, y), (x + w, y + h), box_color, -1)
        cv2.putText(img, btn["label"], (x + 5, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

def check_button_click(x, y):
    for btn in buttons:
        bx, by = btn["pos"]
        if bx < x < bx + 100 and by < y < by + 40:
            return btn["mode"]
    return None

# Main loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_copy = img.copy()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    draw_buttons(img, selected_mode)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            fingers = count_fingers(lm_list)
            total_fingers = sum(fingers)
            x, y = lm_list[8]

            if total_fingers == 1:
                clicked_mode = check_button_click(x, y)
                if clicked_mode:
                    if clicked_mode.startswith("color"):
                        color = (0, 0, 255) if clicked_mode == "color_red" else (0, 0, 0)
                    elif clicked_mode == "quit":
                        cap.release()
                        cv2.destroyAllWindows()
                        exit()
                    else:
                        selected_mode = clicked_mode
                        draw_mode = clicked_mode
                        start_point = None
                        prev_point = None

            if total_fingers > 0:
                if selected_mode == "free" and total_fingers == 1:
                    if prev_point:
                        cv2.line(canvas, prev_point, (x, y), color, 2)
                    prev_point = (x, y)

                elif selected_mode == "line":
                    if not start_point:
                        start_point = (x, y)
                    elif total_fingers == 5:
                        cv2.line(canvas, start_point, (x, y), color, 2)
                        start_point = None
                    elif start_point:
                        cv2.line(img_copy, start_point, (x, y), color, 2)

                elif selected_mode == "rectangle":
                    if not start_point:
                        start_point = (x, y)
                    elif total_fingers == 5:
                        cv2.rectangle(canvas, start_point, (x, y), color, 2)
                        start_point = None
                    elif start_point:
                        cv2.rectangle(img_copy, start_point, (x, y), color, 2)

                elif selected_mode == "erase" and total_fingers == 1:
                    cv2.circle(canvas, (x, y), 30, (0, 0, 0), -1)

                elif selected_mode == "clear" and total_fingers == 1:
                    canvas = np.zeros((720, 1280, 3), np.uint8)
                    selected_mode = None
                    draw_mode = None
                    start_point = None
                    prev_point = None
            else:
                prev_point = None

    # Replace the problematic masking section with this code:
    img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(img_gray, 20, 255, cv2.THRESH_BINARY_INV)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
    # Ensure images have the same dimensions
    mask = cv2.resize(mask, (img.shape[1], img.shape[0]))
    canvas = cv2.resize(canvas, (img.shape[1], img.shape[0]))
    img_copy = cv2.resize(img_copy, (img.shape[1], img.shape[0]))
    
    # Perform the bitwise operations
    img = cv2.bitwise_and(img, mask)
    img = cv2.bitwise_or(img, canvas)
    img = cv2.addWeighted(img, 1, img_copy, 0.5, 0)

    cv2.imshow("Gesture Paint Tool", img)

    # Keyboard quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
