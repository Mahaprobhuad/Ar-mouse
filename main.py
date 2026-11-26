import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

screen_w, screen_h = pyautogui.size()

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

calibrated_horz_min = 0.35
calibrated_horz_max = 0.65
calibrated_vert_min = 0.35
calibrated_vert_max = 0.65


def calibrate():
    print("Starting calibration. Look at the prompts on the screen.")
    instructions = [
        ("Look at the CENTER of the screen.", 2),
        ("Now, look at the TOP-LEFT corner.", 3),
        ("Now, look at the BOTTOM-RIGHT corner.", 3),
        ("Calibration complete!", 2)
    ]

    horz_ratios = []
    vert_ratios = []

    for instruction, duration in instructions:
        start_time = time.time()
        while (time.time() - start_time) < duration:
            success, frame = cap.read()
            if not success:
                continue

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            cv2.putText(frame, instruction, (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('Calibration', frame)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    nose_tip = face_landmarks.landmark[1]

                    nose_x = nose_tip.x
                    nose_y = nose_tip.y

                    horz_ratios.append(nose_x)
                    vert_ratios.append(nose_y)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()
    global calibrated_horz_min, calibrated_horz_max, calibrated_vert_min, calibrated_vert_max

    if horz_ratios and vert_ratios:
        calibrated_horz_min = np.min(horz_ratios)
        calibrated_horz_max = np.max(horz_ratios)
        calibrated_vert_min = np.min(vert_ratios)
        calibrated_vert_max = np.max(vert_ratios)


calibrate()

print("Calibration finished. Starting eye-tracking.")
pyautogui.FAILSAFE = False

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            nose_tip = face_landmarks.landmark[1]

            nose_x = nose_tip.x
            nose_y = nose_tip.y

            if calibrated_horz_max - calibrated_horz_min != 0:
                scaled_x = (nose_x - calibrated_horz_min) / (calibrated_horz_max - calibrated_horz_min)
            else:
                scaled_x = 0.5

            if calibrated_vert_max - calibrated_vert_min != 0:
                scaled_y = (nose_y - calibrated_vert_min) / (calibrated_vert_max - calibrated_vert_min)
            else:
                scaled_y = 0.5

            screen_x = int(scaled_x * screen_w)
            screen_y = int(scaled_y * screen_h)

            screen_x = max(0, min(screen_w, screen_x))
            screen_y = max(0, min(screen_h, screen_y))

            pyautogui.moveTo(screen_x, screen_y)

            x, y = int(nose_x * w), int(nose_y * h)
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    cv2.imshow('Eye Mouse Control', frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
